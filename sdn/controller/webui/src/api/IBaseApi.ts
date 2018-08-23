import {Observable} from 'rxjs';

/**
 * Basic class for api classes, with basic method set.
 *
 * @export
 * @class BaseApi
 */
export interface IBaseApi {
  /**
   * Returns stream with fetched data.
   *
   * @param {string} url
   * @param {object} headers
   * @returns {Observable<any>}
   */
  fetch(url: string, headers?: object): Observable<any>;

  /**
   * Execute http request and returns stream.
   *
   * @param {string} url
   * @param {string} method
   * @param {object} data?
   * @param {object} headers?
   * @returns {Observable<any>}
   */
  ajax(
    url: string,
    method: string,
    data?: object,
    headers?: object,
    responseType?: string,
  ): Observable<any>;
}

export interface TFetchResponse {
  payload?: any;
  totalCount?: number;
}
