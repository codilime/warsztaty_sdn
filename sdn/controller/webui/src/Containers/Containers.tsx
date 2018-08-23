import {inject, observer} from 'mobx-react';
import * as React from 'react';
import {Trans, translate} from 'react-i18next';

import {TranslationFunction} from 'i18next';

import {Button, Card, Col, Icon, Row} from 'antd';

import 'antd/lib/button/style';
import 'antd/lib/card/style';
import 'antd/lib/icon/style';

import {CollectionApi, CollectionStore} from '../api';

import {IConfigStore} from '../config/IConfigStore';
import {IDialogStore} from '../Dialog/IDialogStore';
import {schemaTranslate} from '../Dialog/TranslateSchema';

import Table from '../components/Table';
import TableRowOption from '../components/Table/components/TableRowOption';
import TableRowOptions from '../components/Table/components/TableRowOptions';

import LoadingIndicator from '../components/LoadingIndicator';

import schema from './schema';

interface IProps {
  config: IConfigStore;
  dialog: IDialogStore;
  t?: TranslationFunction;
}

interface IState {
  from: number;
  sortBy: any[];
  to: number;
}

@inject('config', 'dialog')
@observer
export class Containers extends React.Component<IProps, IState> {
  private store;

  constructor(props) {
    super(props);

    const {config} = this.props;

    this.store = new CollectionStore(
      new CollectionApi(
        {serverUrl: config.serverUrl},
        schema,
      ),
    );
  }

  public componentDidMount() {
    this.store.fetch();
  }

  public render() {
    if (this.store.isLoading) {
      return <LoadingIndicator />;
    }

    const {data} = this.store;
    const {t} = this.props;

    return (
      <Card
        title={
          <Row type="flex" justify="space-between">
            <Col span={21}>
              <h4>
                <Trans i18nKey="title" />
              </h4>
            </Col>
            <Col span={3} style={{textAlign: 'right'}}>
              <Button key={1} type="primary" onClick={this.handleCreate}>
                <Icon type="plus" />
                <Trans i18nKey="createButton" />
              </Button>
            </Col>
          </Row>
        }
      >
        <Table
          dataSource={data}
          columns={[
            {
              title: t('table.id'),
              dataIndex: 'id',
            },
            {
              title: '',
              key: 'options',
              render: (text, record) => (
                <TableRowOptions>
                  <TableRowOption
                    type="delete"
                    onClick={() => this.handleRemove(record.id)}
                  />
                </TableRowOptions>
              ),
            },
          ]}
        />
      </Card>
    );
  }

  private handleCreate = async () => {
    this.props.dialog
      .openDialog('createProject', '/container', 'POST', {
        schema: await schemaTranslate(schema.schema, 'projects'),
        title: this.props.t('title'),
      })
      .then(this.store.fetch);
  };

  private handleRemove = (id: string) => {
    this.props.dialog
      .openDialog('removeProject', `/container/${id}`, 'DELETE', {
        message: this.props.t('dialog.remove', {name: id}),
        title: this.props.t('title'),
      })
      .then(this.store.fetch);
  };
}

export default translate('containers')(Containers);
