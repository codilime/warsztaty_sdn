import {IConfig} from './IConfigStore';

export interface IConfigApi {
  /**
   * Returns stream with fetched config data.
   *
   * @returns {Promise<{} | IConfig>}
   */
  fetch(): Promise<{} | IConfig>;
}
