import {action, observable} from 'mobx';

import {IGlobalMessageStore, TGlobalMessage} from './IGlobalMessageStore';

export class GlobalMessageStore implements IGlobalMessageStore {
  @observable public messages = [];

  /**
   * Adds message.
   *
   * @param {string} message
   * @param {string} type - type of message one of:
   *                        success,
   *                        error,
   *                        info,
   *                        warning,
   *                        warn,
   *                        loading.
   */
  @action.bound
  public push(message: string, type: string = 'info') {
    this.messages.push({
      id: this.messages.length,
      message,
      show: true,
      type,
    });
  }

  /**
   * Removes message by specified id.
   *
   * @param {number} id
   */
  @action.bound
  public remove(id: number) {
    const message = this.messages.find(
      (item: TGlobalMessage) => item.id === id,
    );
    if (message) {
      message.show = false;
    } else {
      throw Error(`[GlobalMessageStore.remove] ${id} is wrong message id!`);
    }
  }
}

const globalMessageStore = new GlobalMessageStore();

export default globalMessageStore;
