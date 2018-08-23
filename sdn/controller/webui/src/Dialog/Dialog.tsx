import {Alert, Icon, Modal} from 'antd';
import {Form} from 'gohan-jsonschema-form';
import {observer} from 'mobx-react';
import * as React from 'react';
import {translate} from 'react-i18next';

import 'antd/lib/alert/style';
import 'antd/lib/icon/style';
import 'antd/lib/modal/style';

import {TDialogProps} from './TDialogProps';
import {TDialogState} from './TDialogState';

@observer
export class Dialog extends React.Component<TDialogProps, TDialogState> {
  public static defaultProps = {
    data: {},
    errorMessage: null,
    title: '',
    method: '',
  };

  private form: any;

  constructor(props: TDialogProps) {
    super(props);

    this.state = {
      formData: this.props.data,
    };
  }

  public render(): React.ReactNode {
    const {formData} = this.state;
    const {schema, message, errorMessage, title, t, method} = this.props;

    return (
      <Modal
        visible={this.props.isDialogOpen}
        onCancel={this.handleCloseDialog}
        onOk={this.handleSaveButton}
        confirmLoading={this.props.isInProgress}
        okText={t(`modal.${method}`)}
        cancelText={t('modal.cancel')}
        title={
          <span>
            <Icon type="edit" />
            {title}
          </span>
        }
      >
        {errorMessage && (
          <Alert
            message={errorMessage}
            type={'error'}
            closable={false}
            className={'login-alert'}
          />
        )}
        {message && <div> {message}</div>}
        {schema && (
          <Form
            schema={this.props.schema}
            ref={(c: any) => {
              this.form = c;
            }}
            formData={formData}
          />
        )}
      </Modal>
    );
  }

  private handleCloseDialog: () => void = () => {
    this.props.cancel(this.props.dialogId);
  };

  private handleSaveButton: () => void = () => {
    if (this.form) {
      if (this.form.isValid) {
        this.setState({
          formData: this.form.value,
        });
        this.props.save(this.props.dialogId, this.form.value);
      }
    } else {
      this.props.save(this.props.dialogId);
    }
  };
}

export default translate('app')(Dialog);
