export interface IDialogStore {
  dialogs: TDialog[];
  readonly openedDialogs: TDialog[];

  openDialog(
    dialogId: string,
    url: string,
    method: string,
    additionalProps?: any,
  ): Promise<any>;
  closeDialog(dialogId: string): void;
  startProgress(dialogId: string): void;
  stopProgress(dialogId: string): void;
  execute(dialogId: string, data?: object): void;
}
export interface TDialog {
  dialogId: string;
  isOpen: boolean;
  isInProgress: boolean;
  errorMessage?: string;
  url: string;
  method: string;
  promise: (...args: any[]) => void;
  additionalProps?: any;
}
