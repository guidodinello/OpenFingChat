export const ADD_CHAT_MESSAGE = "ADD_CHAT_MESSAGE";
export const SET_CHAT_LOADING = "SET_CHAT_LOADING";
export const RESET_CHAT = "RESET_CHAT";

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

export type IChatActions =
  | IAddChatMessageAction
  | ISetChatLoadingAction
  | IResetChatAction;
