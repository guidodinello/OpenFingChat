import {
  IQueryActions,
  RESET_QUERY_PARAMS,
  SET_QUERY_PARAMS,
} from "./action-types";

export const setQueryParams = (params: IQuery): IQueryActions => ({
  type: SET_QUERY_PARAMS,
  payload: { params },
});

export const resetQueryParams = (params?: IQuery): IQueryActions => ({
  type: RESET_QUERY_PARAMS,
  payload: { params },
});
