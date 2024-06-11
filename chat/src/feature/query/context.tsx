"use client";
import {
  Dispatch,
  ReactNode,
  createContext,
  useContext,
  useReducer,
} from "react";
import queryReducer, { initialState } from "./reducer";
import { IQueryActions } from "./action-types";

// context
const QueryContext = createContext<{
  state: IQuery;
  dispatch: Dispatch<IQueryActions>;
}>({ state: initialState, dispatch: () => null });

// provider
const QueryProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(queryReducer, initialState);

  return (
    <QueryContext.Provider value={{ state, dispatch }}>
      {children}
    </QueryContext.Provider>
  );
};

// hook
const useQuery = () => {
  return useContext(QueryContext);
};

export default QueryContext;
export { QueryProvider, useQuery };
