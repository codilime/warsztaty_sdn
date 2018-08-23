import {inject, observer} from 'mobx-react';
import * as React from 'react';

import {DialogStore} from './DialogStore';

import Dialog from './Dialog';
import {IDialogStore, TDialog} from './IDialogStore';

interface IDialogsProps {
  dialog?: IDialogStore;
}

@inject('dialog')
@observer
export default class Dialogs extends React.Component<IDialogsProps> {
  private handleCloseDialog: (id: string) => void = id => {
    this.props.dialog.closeDialog(id);
  };

  private handleSave: (id: string, data?: object) => void = (id, data) => {
    this.props.dialog.execute(id, data);
  };

  public render() {
    // tslint:disable-line
    const {openedDialogs} = this.props.dialog;

    return openedDialogs.map((item: TDialog) => (
      <Dialog
        key={item.dialogId}
        dialogId={item.dialogId}
        isDialogOpen={item.isOpen}
        method={item.method}
        isInProgress={item.isInProgress}
        errorMessage={item.errorMessage}
        cancel={this.handleCloseDialog}
        save={this.handleSave}
        {...item.additionalProps}
      />
    ));
  }
}
