import React from "react";
import {connect} from 'react-redux'
import {getPosts,deletePost,uploadFile} from '../Redux/actions.js'


class UploadAudioFile extends React.Component {

    componentDidMount() {
    }

    state = {
        selectedFile: null
    }

    onFileChange = event => {
        this.setState({ selectedFile: event.target.files[0] });
    }

    onFileUpload = () => {
        const formData = new FormData();

        formData.append("file", this.state.selectedFile);
        formData.append("name", this.state.selectedFile.name);

        console.log(this.state.selectedFile);

        this.props.uploadFile(formData);
    }

    fileData = () => {

        if (this.state.selectedFile) {

            return (
                <div>
                    <h2>File Details:</h2>
                    <p>File Name: {this.state.selectedFile.name}</p>
                    <p>File Type: {this.state.selectedFile.type}</p>
                    <p>
                        Last Modified:{" "}
                        {this.state.selectedFile.lastModifiedDate.toDateString()}
                    </p>
                </div>
            );
        } else {
            return (
                <div>
                    <br/>
                    <h4>Choose before Pressing the Upload button</h4>
                </div>
            );
        }
    };

    render() {
        return (
            <div>
                <div>
                    <h1>
                        Scooby
                    </h1>
                    <h3>
                        Upload your audio file to practice!
                    </h3>
                    <div>
                        <input type="file" onChange={this.onFileChange} />
                        <button onClick={this.onFileUpload}>
                            Upload!
                        </button>
                    </div>
                    {this.fileData()}
                </div>
            </div>
        );
    }
}

const mapStateToProps = (state) => ({
    posts: state.posts,
    stt_result: state.stt_result
})

const mapDispatchToProps = {
    getPosts ,deletePost, uploadFile
}

export default connect(mapStateToProps, mapDispatchToProps)(UploadAudioFile)