import {BaseApi} from '../api';

import {IDialogApi} from './IDialogApi';

export class DialogApi extends BaseApi implements IDialogApi {
  public executeRequest(url, method, data?) {
    return new Promise<boolean>((resolve, reject) => {
      this.ajax(
        url,
        method,
        data,
      ).subscribe(
        () => {
          resolve(true);
        },
        (error: Error) => {
          reject(error);
        },
      );
    });
  }
}
