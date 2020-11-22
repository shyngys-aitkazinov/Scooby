import Types from "./types";
const initialState = {
    posts: [],
    loading:false,
    stt_result: ""
};

const postReducer = (state = initialState, action) => {
    switch (action.type) {
        case Types.POSTS_LOADING: {
            console.log("create_item");
            return {...state,loading: action.payload};
        }

        case Types.GET_POSTS: {
            return {...state,posts: action.payload};
        }

        case Types.DELETE_POST: {
            return {...state, posts: state.posts.filter(post => post.id != action.payload)}
        }

        case Types.UPLOAD_FILE: {
            return {...state, stt_result: action.payload.stt_result};
        }
        default:
            return state;
    }
}

export default postReducer;