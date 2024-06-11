import {
  IChatActions,
  ADD_CHAT_MESSAGE,
  SET_CHAT_LOADING,
  RESET_CHAT,
} from "./action-types";

const initialState: IChat = {
  messages: [],
  loading: false,
};

const chatReducer = (
  state: IChat = initialState,
  action: IChatActions
): IChat => {
  switch (action.type) {
    case ADD_CHAT_MESSAGE:
      return {
        ...state,
        messages: [...state.messages, action.payload.message],
      };
    case SET_CHAT_LOADING:
      return { ...state, loading: action.payload.loading };
    case RESET_CHAT:
      return initialState;
    default:
      return state;
  }
};

export default chatReducer;
export { initialState };
