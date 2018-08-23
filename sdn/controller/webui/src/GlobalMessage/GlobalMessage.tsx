import {message} from 'antd';
import {reaction} from 'mobx';
import {observer} from 'mobx-react';
import * as React from 'react';

import 'antd/lib/message/style';

import globalMessageStore from './GlobalMessageStore';
import {IGlobalMessageStore, TGlobalMessage} from './IGlobalMessageStore';

interface IProps {
  globalMessageStore: IGlobalMessageStore;
}
@observer
class GlobalMessage extends React.Component<IProps> {
  protected messageReaction: any;

  public componentDidMount(): void {
    this.messageReaction = reaction(
      () =>
        this.props.globalMessageStore.messages.filter(
          (item: TGlobalMessage) => item.show,
        ),
      (messages: TGlobalMessage[]) => {
        messages.forEach((item: TGlobalMessage) => {
          try {
            globalMessageStore.remove(item.id);
            message[item.type](item.message);
          } catch (error) {
            message.error(`"${item.type}" is wrong global message type!`);
          }
        });
      },
    );
  }

  public componentWillUnmount(): void {
    this.messageReaction();
  }

  public render(): null {
    return null;
  }
}

export default GlobalMessage;
