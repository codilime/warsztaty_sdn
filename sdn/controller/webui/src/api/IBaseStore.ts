/**
 * Basic class for store classes, with basic method set.
 *
 * @export
 * @class BaseStore
 */
export interface IBaseStore {
  /**
   * Returns loading state.
   *
   * @readonly
   * @return {boolean} - if true loading is in progress, otherwise is done.
   */
  readonly isLoading: boolean;

  /**
   * Observable error message.
   *
   * @type {string}
   */
  errorMessage: string;

  /**
   * Fetch data form backend. (not implemented)
   */
  fetch(...args: any[]): void | never;

  /**
   * Stops runned polling.
   */
  stopPolling(): void;

  /**
   * Starts polling loop.
   */
  startPolling(): void;
}
