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
