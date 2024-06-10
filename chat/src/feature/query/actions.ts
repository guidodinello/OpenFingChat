export const setQueryParams = (params: IQuery): IQueryActions => ({
  type: SET_QUERY_PARAMS,
  payload: { params },
});

export const setExtraParams = (params?: IQuery): IQueryActions => ({
  type: RESET_QUERY_PARAMS,
  payload: { params },
});
