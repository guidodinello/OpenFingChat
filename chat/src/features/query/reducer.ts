import {
  IQueryActions,
  RESET_QUERY_PARAMS,
  SET_QUERY_PARAMS,
} from "./action-types";

const initialState: IQuery = {
  query: "",
  subject: undefined,
  lesson: undefined,
};

const queryReducer = (
  state: IQuery = initialState,
  action: IQueryActions
): IQuery => {
  switch (action.type) {
    case SET_QUERY_PARAMS:
      return { ...state, ...action.payload.params };
    case RESET_QUERY_PARAMS:
      return { ...initialState, ...(action.payload.params || {}) };
    default:
      return state;
  }
};

export default queryReducer;
export { initialState };
