const SET_QUERY_PARAMS = "SET_QUERY_PARAMS";
const RESET_QUERY_PARAMS = "RESET_QUERY_PARAMS";

interface ISetQueryParamAction {
  type: typeof SET_QUERY_PARAMS;
  payload: { params: IQuery };
}

interface IResetQueryParamsAction {
  type: typeof RESET_QUERY_PARAMS;
  payload: { params?: IQuery };
}

type IQueryActions = ISetQueryParamAction | IResetQueryParamsAction;
