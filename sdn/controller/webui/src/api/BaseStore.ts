import {action, computed, observable} from 'mobx';
import {toStream} from 'mobx-utils';
import {Observable} from 'rxjs/Rx';

import {BaseApi, IBaseApi, IBaseStore} from './';

/**
 * Basic class for store classes, with basic method set.
 *
 * @class BaseStore
 */
export class BaseStore implements IBaseStore {
  /**
   * Observable error message.
   * @type {string}
   */
  @observable public errorMessage = '';

  /**
   * Loading state, if true loading is in progress, otherwise is done.
   *
   * @type {boolean}
   */
  @observable protected loadingState = true;

  /**
   * Observable state of polling.
   * @type {boolean}
   */
  @observable protected isPollingOn = true;

  /**
   * API object
   */
  protected api;

  /**
   * Stream object
   */
  protected stream;

  /**
   * Creates an instance of BaseStore.
   *
   * @param {BaseApi} api
   */
  constructor(api: any) {
    if (!api) {
      throw new Error('BaseStore: Api object is required!');
    }

    this.api = api;
  }

  /**
   * Returns loading state.
   *
   * @returns {boolean}
   */
  @computed
  get isLoading() {
    return this.loadingState;
  }

  /**
   * Stops runned polling.
   *
   * @memberof BaseStore
   */
  @action.bound
  public stopPolling() {
    this.isPollingOn = false;
  }

  /**
   * Starts polling loop.
   *
   * @memberof BaseStore
   */
  @action.bound
  public startPolling() {
    this.stream = Observable.timer(10000, 10000) // TODO
      .takeUntil(Observable.from(toStream(() => this.isPollingOn)));
    this.stream.subscribe(this.fetch);
  }

  /**
   * Fetch data from backend. (not implemented)
   *
   * @memberof BaseStore
   */
  public fetch(...args: any[]) {
    throw new Error('BaseStore: Please implement fetch method!');
  }
}
