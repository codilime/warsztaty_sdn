import {AjaxError, AjaxResponse, Observable} from 'rxjs';
import {ajax} from 'rxjs/observable/dom/ajax';

import {BaseApi} from '../api';
import {IConfigApi} from './IConfigApi';
import {IConfig} from './IConfigStore';

export class ConfigApi implements IConfigApi {
  public fetch() {
    return new Promise((resolve, reject) => {
      ajax({
        crossDomain: true,
        headers: {
          'Content-Type': 'application/json',
        },
        method: 'GET',
        url: './config.json',
      })
        .map(
          (response: AjaxResponse): IConfig => {
            const result = {...response.response};

            if (result.serverUrl.includes('__HOST__')) {
              result.serverUrl = result.serverUrl.replace(
                '__HOST__',
                location.hostname,
              );
            }

            return result;
          },
        )
        .catch((error: AjaxError) => {
          throw BaseApi.parseXHRError(error);
        })
        .subscribe(
          (data: IConfig) => {
            resolve(data);
          },
          (error: Error) => {
            reject(error);
          },
        );
    });
  }
}
