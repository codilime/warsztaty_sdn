import {IBaseApi} from '../api';

export interface IDialogApi extends IBaseApi {
  executeRequest(url: string, method: string, data?: object): Promise<any>;
}
