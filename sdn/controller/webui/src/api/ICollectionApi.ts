import {IBaseApi, TFetchResponse} from './';

export interface ICollectionApi extends IBaseApi {
  fetchCollection(search?: object, headers?: object): Promise<TFetchResponse>;
}
