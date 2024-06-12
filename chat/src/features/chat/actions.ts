import { Dispatch } from "react";
import {
  IChatActions,
  ADD_CHAT_MESSAGE,
  SET_CHAT_LOADING,
  RESET_CHAT,
} from "./action-types";
import ChatAPI from "./api";

export const addChatMessage = (message: IMessage): IChatActions => ({
  type: ADD_CHAT_MESSAGE,
  payload: { message },
});

export const setChatLoading = (loading: boolean = false): IChatActions => ({
  type: SET_CHAT_LOADING,
  payload: { loading },
});

export const resetChat = (): IChatActions => ({
  type: RESET_CHAT,
});

export const sendMessage = (
  query: IQuery,
  dispatch: Dispatch<IChatActions>
) => {
  dispatch(setChatLoading(true));
  dispatch(addChatMessage({ message: query.query || "", sources: [] }));

  return ChatAPI.send(query).then((response) => {
    dispatch(setChatLoading(false));
    dispatch(addChatMessage(response.data));

    return response;
  });
};

const showError = (msg: string) => alert(msg);
