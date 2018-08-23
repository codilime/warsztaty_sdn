import {action, observable} from 'mobx';

import {IConfig, IConfigStore} from './IConfigStore';

export default class ConfigStore implements IConfigStore {
  @observable public authDomain = '';
  @observable public serverUrl = '';
  @observable public isLoading = true;
  @observable public filteredRoles = [];
  protected api = undefined;

  /**
   * Creates an instance of ConfigStore.
   *
   * @param {IConfigApi} api
   */
  constructor(api: any) {
    if (!api) {
      throw new Error('[ConfigStore]: Api object is required!');
    }

    this.api = api;
  }

  @action.bound
  public async fetch() {
    try {
      const data = await this.api.fetch();

      this.authDomain = data.authDomain;
      this.serverUrl = data.serverUrl;
      this.filteredRoles = data.filteredRoles;
    } catch (error) {
      throw new Error(`[ConfigStore]: ${error}`);
    }
    this.isLoading = false;
  }
}
