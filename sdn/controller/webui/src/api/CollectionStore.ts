import {action, observable} from 'mobx';

import {globalMessageStore} from '../GlobalMessage';
import {BaseStore} from './';
import {ICollectionStore} from './ICollectionStore';

export class CollectionStore extends BaseStore implements ICollectionStore {
  @observable public data = [];
  @observable public totalCount = 0;
  @observable public query = {};

  @action.bound
  public async fetch(query, headers?) {
    try {
      Object.assign(this.query, query);
      const data = await this.api.fetchCollection(this.query, headers);

      this.data = data.payload;
      this.totalCount = data.totalCount;
    } catch (error) {
      this.errorMessage = error;
      globalMessageStore.push(error, 'error');
    }
    this.loadingState = false;
  }
}
