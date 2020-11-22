import React from 'react';
import {connect} from 'react-redux'
import { } from '../Redux/actions.js'
import {Box, Text, Heading} from 'grommet'

class Practice extends React.Component {
    render() {
        const stt_result = this.props.stt_result

        return (
            <Box>
                <Heading>Result</Heading>
                <Text>{stt_result}</Text>
            </Box>
        );
    }
}

const mapStateToProps = (state) => ({
    stt_result: state.stt_result
})

const mapDispatchToProps = {}

export default connect(mapStateToProps, mapDispatchToProps)(Practice)