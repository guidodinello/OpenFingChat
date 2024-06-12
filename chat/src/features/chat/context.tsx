"use client";
import {
  Dispatch,
  ReactNode,
  createContext,
  useContext,
  useReducer,
} from "react";
import queryReducer, { initialState } from "./reducer";
import { IChatActions } from "./action-types";

// context
const ChatContext = createContext<{
  state: IChat;
  dispatch: Dispatch<IChatActions>;
}>({ state: initialState, dispatch: () => null });

// provider
const ChatProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(queryReducer, initialState);

  return (
    <ChatContext.Provider value={{ state, dispatch }}>
      {children}
    </ChatContext.Provider>
  );
};

// hook
const useChat = () => {
  return useContext(ChatContext);
};

export default ChatContext;
export { ChatProvider, useChat };
