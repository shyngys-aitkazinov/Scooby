import React from "react";
import { Button, Box, Header, Heading, Grommet, ResponsiveContext, Text } from 'grommet';
// import {Layout, Menu} from 'antd';
// import "antd/dist/antd.css";
import ListPosts from "./ListPosts";
// import CreateNewPost from "./CreateNewPost";

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
            selected:1
        }
    }
    handleClick = e => {
        this.setState({selected:e})
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
                            <ListPosts />
                        </Box>
                    )}
                </ResponsiveContext.Consumer>
            </Grommet>
        )
        // const { Header, Content } = Layout;
        //
        // return (
        //     <Layout>
        //         <Header>
        //             <Menu theme="dark" mode="horizontal" defaultSelectedKeys={[this.state.selected.toString()]}>
        //                 <Menu.Item key="1" onClick={() => this.handleClick(1)}> Read Posts</Menu.Item>
        //                 <Menu.Item key="2" onClick={() => this.handleClick(2)}> Create Post</Menu.Item>
        //             </Menu></Header>
        //         <Content>
        //             {this.state.selected==1?<ListPosts />: <CreateNewPost />
        //             }
        //         </Content>
        //     </Layout>
        // );
    }
}


export default Scooby