import {AjaxError, AjaxResponse, Observable} from 'rxjs';
import {ajax} from 'rxjs/observable/dom/ajax';

import {IBaseApi, TFetchResponse} from './';

/**
 * Basic class for api classes, with basic method set.
 *
 * @export
 * @class BaseApi
 */
export class BaseApi implements IBaseApi {
  /**
   * Parses error message to human readability.
   *
   * @param  {AjaxError} error - Error object or error string message.
   * @return string  - parsed error message.
   * @memberof BaseApi
   */
  public static parseXHRError(error: AjaxError): string {
    if (error) {
      if (error.xhr) {
        if (error.xhr.response) {
          const {response} = error.xhr;

          if (typeof response === 'object') {
            if (response.error) {
              const {error: responseError} = response;

              if (typeof responseError === 'object') {
                if (responseError.message) {
                  if (typeof responseError.message === 'string') {
                    return responseError.message;
                  }
                }
              } else if (typeof responseError === 'string') {
                return responseError;
              }
            }
          } else if (typeof response === 'string') {
            return response;
          }
        }
      } else if (error.message) {
        return error.message;
      }
    }
    return 'Unknown error!';
  }

  private serverUrl: string;

  /**
   * Creates an instance of BaseApi.
   *
   * @param {Object} options - Options object.
   * @param {string} options.token - api token.
   * @param {string} options.serverUrl - url to backend server
   * @memberof BaseApi
   */
  constructor(options) {
    if (!options.serverUrl) {
      throw new Error('[BaseApi]: Server address is undefined!');
    }
    this.serverUrl = options.serverUrl;
  }

  /**
   * Returns stream with fetched data.
   *
   * @param {string} url
   * @param {object} headers
   * @returns {Observable<any>}
   */
  public fetch(url, headers?) {
    return ajax({
      crossDomain: true,
      headers: {
        accept: 'application/json',
        'content-type': 'application/json',
        ...headers,
      },
      method: 'GET',
      url: `${this.serverUrl}${url}`,
    })
      .map(
        (response: AjaxResponse): TFetchResponse => ({
          payload: response.response,
        }),
      )
      .catch((error: AjaxError) => {
        throw BaseApi.parseXHRError(error);
      });
  }

  public ajax(url, method, data?, headers?, responseType?) {
    return ajax({
      body: data,
      crossDomain: true,
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        ...headers,
      },
      method,
      responseType,
      url: `${this.serverUrl}${url}`,
    })
      .map((response: AjaxResponse) => response.response)
      .catch((error: AjaxError) => {
        throw BaseApi.parseXHRError(error);
      });
  }
}
