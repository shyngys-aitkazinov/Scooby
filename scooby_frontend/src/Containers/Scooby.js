import React from "react";
import { Button, Box, Header, Heading, Grommet, ResponsiveContext, Text } from 'grommet';
import ListPosts from "./ListPosts";
import UploadAudioFile from "./UploadAudioFile";
import Practice from "./Practice";

const theme = {
    global: {
        colors: {
            // background: '#f8f7f5',
            brand: '#fc4444',
            // active: '#436c00',
            // focus: '#436c00',
            // bullet: '#436c00',
            // highlight: '#b1ca80',
        },
        // font: {
        //     family: 'Lato, Helvetica Neue',
        //     size: '14px',
        //     height: '20px',
        // },
        // "::selection": '#18aa94',
    },
};

class Scooby extends React.Component {
    constructor(props) {
        super(props);
        this.state = {

        }
    }

    render() {
        return (
            <Grommet theme={theme} full>
                <ResponsiveContext.Consumer>
                    {size => (
                        <Box fill={true}>
                            <Header background={"brand"}>
                                <Button margin={"small"}>Scooby</Button>
                            </Header>
                            <UploadAudioFile />
                            <Practice />
                        </Box>
                    )}
                </ResponsiveContext.Consumer>
            </Grommet>
        )
    }
}

export default Scooby