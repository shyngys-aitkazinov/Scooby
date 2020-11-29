from __future__ import absolute_import, division, print_function

import numpy as np
import shlex
import subprocess
import sys
import wave
import json
from deepspeech import Model, version
from timeit import default_timer as timer
import io
import soundfile as sf
import os

# Import libraries
from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech
# from google.cloud import speech

try:
    from shhlex import quote
except ImportError:
    from pipes import quote


model_file_path = os.path.join(".", "STT_models", 'deepspeech-0.8.1-models.pbmm')
scorer_file_path = os.path.join(".", "STT_models", 'deepspeech-0.8.1-models.scorer')
# audio_path = "audio/2830-3980-0043.wav"


def convert_samplerate(audio_path, desired_sample_rate):
    sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate {} --encoding signed-integer --endian little --compression 0.0 --no-dither - '.format(quote(audio_path), desired_sample_rate)
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
    except OSError as e:
        raise OSError(e.errno, 'SoX not found, use {}hz files or install it: {}'.format(desired_sample_rate, e.strerror))

    return desired_sample_rate, np.frombuffer(output, np.int16)


def metadata_to_string(metadata):
    return ''.join(token.text for token in metadata.tokens)

def mp3_to_wav(audio_file_name):
    if audio_file_name.split('.')[1] == 'mp3':    
        sound = AudioSegment.from_mp3(audio_file_name)
        audio_file_name = audio_file_name.split('.')[0] + '.wav'
        sound.export(audio_file_name, format="wav")

def frame_rate_channel(audio_file_name):
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return frame_rate,channels

def stereo_to_mono(audio_file_name):
    sound = AudioSegment.from_wav(audio_file_name)
    sound = sound.set_channels(1)
    sound.export(audio_file_name, format="wav")

def words_from_candidate_transcript(metadata):
    word = ""
    word_list = []
    word_start_time = 0
    # Loop through each character
    for i, token in enumerate(metadata.tokens):
        # Append character to word if it's not a space
        if token.text != " ":
            if len(word) == 0:
                # Log the start time of the new word
                word_start_time = token.start_time

            word = word + token.text
        # Word boundary is either a space or the last character in the array
        if token.text == " " or i == len(metadata.tokens) - 1:
            word_duration = token.start_time - word_start_time

            if word_duration < 0:
                word_duration = 0

            each_word = dict()
            each_word["word"] = word
            each_word["start_time"] = round(word_start_time, 4)
            each_word["duration"] = round(word_duration, 4)

            word_list.append(each_word)
            # Reset
            word = ""
            word_start_time = 0

    return word_list


def metadata_json_output(metadata):
    json_result = dict()
    json_result["transcripts"] = [{
        "confidence": transcript.confidence,
        "words": words_from_candidate_transcript(transcript),
    } for transcript in metadata.transcripts]
    return json.dumps(json_result, indent=2)


def MozillaSTT(audio_path):

    # TODO: handle different rates (not implemented)
    fin = wave.open(audio_path, 'rb')
    output = ""
    # print("SS")
    ds = Model(model_file_path)
    # print("SS")
    ds.enableExternalScorer(scorer_file_path)
    # print("SS")

    lm_alpha = 0.75  # ??
    lm_beta = 1.85
    desired_sample_rate = ds.sampleRate()
    ds.setScorerAlphaBeta(lm_alpha, lm_beta)
    fs_orig = fin.getframerate()
    # print("Desired Sampling Rate: %d", desired_sample_rate)
    if fs_orig != desired_sample_rate:
        print('Warning: original sample rate ({}) is different than {}hz. \
Resampling might produce erratic speech   recognition.'.format(fs_orig, desired_sample_rate), file=sys.stderr)
        fs_new, audio = convert_samplerate(audio_path, desired_sample_rate)
    else:
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

    # audio_length = fin.getnframes() * (1/fs_orig)
    fin.close()
    print('Running inference.', file=sys.stderr)
    # print(metadata_to_string(ds.sttWithMetadata(audio, 1).transcripts[0]))
    # print(metadata_json_output(ds.sttWithMetadata(audio, 3)))
    # print(ds.stt(audio))
    output += ds.stt(audio)
    output += '\n'
    output += metadata_json_output(ds.sttWithMetadata(audio, 3))
    return output


def google_transcribe(audio_file_path):
    
    file_name = audio_file_path
    # mp3_to_wav(file_name)

    # The name of the audio file to transcribe
    frame_rate, channels = frame_rate_channel(file_name)
    
    if channels > 1:
        stereo_to_mono(file_name)
    

    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
    
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content = content)

    config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,sample_rate_hertz=frame_rate,
        language_code='en-US',
        enable_word_confidence=True)
    # config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,             sample_rate_hertz=frame_rate,
    # language_code='en-US'
    # )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)
    # print(response)
    
    return response


def simple_word_scorer(script, response):
    detected_word_sequence = []
    detected_word_dict = dict()
    for word in (response.results[0].alternatives[0].words):
        detected_word_sequence.append((word.word, word.confidence))
        if word.word in detected_word_dict.keys():
            detected_word_dict[word.word].append(word.confidence)
        else:
            detected_word_dict[word.word] = [word.confidence]
    
    # word_checking_interval = 4
    score = 0.0
    counter = 0
    taken_list,undetected_list = [], []
    for w in detected_word_sequence:
        taken_list.append([True, w])
    for w in script[1]:
        undetected_list.append([True, w])
    # loop over sript
    for j in range(len(script[0])):
        script_word = script[0][j]
        # loop over detected
        # print("**", script_word)
        for i in range(max(0, counter - 1),  min(counter + 2, len(detected_word_sequence))):
            detected_word = detected_word_sequence[i][0]
            # print("det_", detected_word)
            if type(script_word) == list:
                if detected_word in script_word  and taken_list[i]:
                    taken_list[i][0] = False
                    undetected_list[j][0] = False
                    score += detected_word_sequence[i][1]
                    break
            else:
                if script_word == detected_word and taken_list[i]:
                    # print("!@#")
                    undetected_list[j][0] = False
                    taken_list[i][0] = False 
                    score += detected_word_sequence[i][1]
                    break
        counter += 1
       
    return taken_list, undetected_list, 100*score/len(script_word[0])
                
                
def script_converter(raw_script):
    punctuation_signs = '.,:;!()?-"'
    apostrophe = "'"
    # hyphen = "-"
    raw_script_copy = list(raw_script[:])
    
    for i in range(len(raw_script_copy)):
        if raw_script_copy[i] in punctuation_signs:
            raw_script_copy[i] = ' '
    raw_script_copy =  "".join(raw_script_copy)   

    raw_script_list = raw_script_copy.strip().split()
    raw_script_list_processed = []

    for i in range(len(raw_script_list)):
        if apostrophe in raw_script_list[i]:
            if apostrophe == raw_script_list[i][-2] and raw_script_list[i][-1] == 's':
                temp_word = raw_script_list[i][0:-2].lower()
                raw_script_list_processed.append([temp_word, temp_word+"s", temp_word+"'s"])

            elif apostrophe == raw_script_list[i][-1]:
                temp_word = raw_script_list[i][0:-1].lower()
                raw_script_list_processed.append([temp_word, temp_word+"'"])
            else:
                raw_script_list_processed.append(raw_script_list[i].replace("'",'').lower())

        else:
            raw_script_list_processed.append(raw_script_list[i].lower())
    # print(raw_script_list_processed)
    return raw_script_list_processed, raw_script_list

# if __name__ == "__main__":
#     MozillaSTT(wave.open(audio_path, 'rb'))