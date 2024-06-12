export const SET_QUERY_PARAMS = "SET_QUERY_PARAMS";
export const RESET_QUERY_PARAMS = "RESET_QUERY_PARAMS";

interface ISetQueryParamAction {
  type: typeof SET_QUERY_PARAMS;
  payload: { params: IQuery };
}

interface IResetQueryParamsAction {
  type: typeof RESET_QUERY_PARAMS;
  payload: { params?: IQuery };
}

export type IQueryActions = ISetQueryParamAction | IResetQueryParamsAction;
