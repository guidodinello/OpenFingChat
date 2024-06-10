const ADD_CHAT_MESSAGE = "ADD_CHAT_MESSAGE";
const SET_CHAT_LOADING = "SET_CHAT_LOADING";
const RESET_CHAT = "RESET_CHAT";

interface IAddChatMessageAction {
  type: typeof ADD_CHAT_MESSAGE;
  payload: { message: IMessage };
}

interface ISetChatLoadingAction {
  type: typeof SET_CHAT_LOADING;
  payload: { loading: boolean };
}

interface IResetChatAction {
  type: typeof RESET_CHAT;
}

type IChatActions =
  | IAddChatMessageAction
  | ISetChatLoadingAction
  | IResetChatAction;