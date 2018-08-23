import {action, computed, observable} from 'mobx';

import {IDialogApi} from './IDialogApi';
import {IDialogStore, TDialog} from './IDialogStore';

export class DialogStore implements IDialogStore {
  protected static allowedMethods: string[] = [
    'POST',
    'PUT',
    'DELETE',
    'PATCH',
  ];

  @observable public dialogs = [];

  /**
   * API object
   */
  protected api;

  constructor(api: IDialogApi) {
    if (!api) {
      throw new Error('[DialogStore]: Api object is required!');
    }

    this.api = api;
  }

  @action.bound
  public openDialog(dialogId, url, method, additionalProps?) {
    return new Promise(resolve => {
      const dialog = this.getDialog(dialogId);

      if (dialog) {
        dialog.isOpen = true;
        dialog.isInProgress = false;
        dialog.url = url;
        dialog.method = method;
        dialog.additionalProps = additionalProps;
        dialog.errorMessage = null;
        dialog.promise = resolve;
      } else {
        this.dialogs.push({
          additionalProps,
          dialogId,
          errorMessage: null,
          isInProgress: false,
          isOpen: true,
          method,
          promise: resolve,
          url,
        });
      }
    });
  }

  @action.bound
  public closeDialog(dialogId) {
    const dialog = this.getDialog(dialogId);

    if (dialog) {
      dialog.isOpen = false;
      dialog.isInProgress = false;
      dialog.errorMessage = null;
    } else {
      throw new Error(`[DialogStore]: Dialog \'${dialogId}\' doesn\'t exit!`);
    }
  }

  @action.bound
  public async execute(dialogId, data) {
    const dialog = this.getDialog(dialogId);

    if (!dialog) {
      throw new Error(`[DialogStore]: Dialog \'${dialogId}\' doesn\'t exit!`);
    } else if (!dialog.isOpen) {
      throw new Error(`[DialogStore]: Dialog \'${dialogId}\' doesn\'t open!`);
    } else if (dialog.isInProgress) {
      throw new Error(
        `[DialogStore]: Dialog \'${dialogId}\' is in progress state!`,
      );
    }

    if (DialogStore.allowedMethods.includes(dialog.method)) {
      try {
        this.startProgress(dialogId);
        await this.api.executeRequest(dialog.url, dialog.method, data);
        dialog.promise();
        this.closeDialog(dialogId);
      } catch (error) {
        dialog.errorMessage = error;
        this.stopProgress(dialogId);
      }
    } else {
      throw new Error(
        `[DialogStore]: \'${dialog.method}\' doesn't valid method type!`,
      );
    }
  }

  @action.bound
  public startProgress(dialogId) {
    const dialog = this.getDialog(dialogId);

    if (dialog) {
      if (dialog.isOpen) {
        dialog.isInProgress = true;
      } else {
        throw new Error(`[DialogStore]: Dialog \'${dialogId}\' is closed!`);
      }
    } else {
      throw new Error(`[DialogStore]: Dialog \'${dialogId}\' doesn\'t exit!`);
    }
  }

  @action.bound
  public stopProgress(dialogId) {
    const dialog = this.getDialog(dialogId);

    if (dialog) {
      if (dialog.isOpen) {
        dialog.isInProgress = false;
      } else {
        throw new Error(`[DialogStore]: Dialog \'${dialogId}\' is closed!`);
      }
    } else {
      throw new Error(`[DialogStore]: Dialog \'${dialogId}\' doesn\'t exit!`);
    }
  }

  @computed
  public get openedDialogs() {
    return this.dialogs.filter((item: TDialog) => item.isOpen);
  }

  public getDialog(dialogId) {
    return this.dialogs.find((item: TDialog) => item.dialogId === dialogId);
  }
}
