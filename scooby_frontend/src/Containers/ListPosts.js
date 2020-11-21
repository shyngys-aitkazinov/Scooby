import React from "react";
import {connect} from 'react-redux'
import {getPosts,deletePost} from '../Redux/actions.js'
import {Box, Text} from 'grommet'


class ListPosts extends React.Component {

    componentDidMount() {
        this.props.getPosts();
    }

    deletePost = (id) => {
        this.props.deletePost(id, this.info);
    }

    info() {

    };

    render() {
        const posts = this.props.posts
        console.log(posts)

        return (
            <Box>
                {posts.map(p => (
                    <Text margin={"large"}>{p.content}</Text>
                    // <Row gutter={[48, 48]}>
                    //     <Col span={24}>
                    //         <Card
                    //             key={p.id}
                    //             title={p.title}
                    //             style={{width: '100%'}}
                    //             actions={[
                    //                 <DeleteOutlined key="delete" onClick={()=>this.deletePost(p.id)} />,
                    //             ]}
                    //         >
                    //             <p>{p.content}</p>
                    //         </Card>
                    //     </Col>
                    // </Row>
                ))}
            </Box>
        );
    }
}

const mapStateToProps = (state) => ({
    posts: state.posts
})

const mapDispatchToProps = {
    getPosts ,deletePost
}

export default connect(mapStateToProps, mapDispatchToProps)(ListPosts)