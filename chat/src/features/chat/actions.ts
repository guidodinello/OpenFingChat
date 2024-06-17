import { Dispatch } from "react";
import {
  IChatActions,
  ADD_CHAT_MESSAGE,
  SET_CHAT_LOADING,
  RESET_CHAT,
} from "./action-types";
import ChatAPI from "./api";
import { IQueryActions } from "../query/action-types";
import { setQueryParams } from "../query/actions";

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
  dispatch: Dispatch<IChatActions>,
  dispatchQuery: Dispatch<IQueryActions>
) => {
  dispatch(setChatLoading(true));
  dispatchQuery(setQueryParams({ query: "" }));
  dispatch(addChatMessage({ message: query.query || "", sources: [] }));

  return ChatAPI.send(query).then((response) => {
    dispatch(setChatLoading(false));
    dispatch(addChatMessage(response.data));
    dispatchQuery(setQueryParams({ conversationId: response.conversationId }));
    return response;
  });
};

const showError = (msg: string) => alert(msg);
