import {inject, observer, Provider} from 'mobx-react';
import * as React from 'react';
import {withRouter} from 'react-router-dom';

import {Layout as AntLayout} from 'antd';

import {IConfigStore} from '../config/IConfigStore';
import {DialogApi} from '../Dialog/DialogApi';
import {DialogStore} from '../Dialog/DialogStore';

import Dialogs from '../Dialog/Dialogs';
import Header from './components/Header/Header';
import Sider from './components/Sidebar/Sider';

import 'antd/lib/layout/style';

import 'gohan-jsonschema-form/lib/style.css';

interface IProps {
  config: IConfigStore;
  children: React.ReactNode;
}

interface IState {
  openUserMenu: boolean;
  openSidebar: boolean;
}

@inject('config')
@observer
class App extends React.Component<IProps, IState> {
  private dialogStore;
  constructor(props) {
    super(props);

    this.state = {
      openSidebar: true,
      openUserMenu: false,
    };

    this.dialogStore = new DialogStore(
      new DialogApi({
        serverUrl: this.props.config.serverUrl,
      }),
    );
  }

  private handleToggleSidebar = () => {
    if (this.state.openSidebar) {
      this.setState({
        openSidebar: false,
      });
    } else {
      this.setState({
        openSidebar: true,
      });
    }
  };

  public render() {
    // tslint:disable-line
    const {children} = this.props;

    return (
      <AntLayout className={'cpe-app'}>
        <Sider isSidebarOpen={this.state.openSidebar} />
        <AntLayout>
          <Header
            onToggleSidebar={this.handleToggleSidebar}
            isSidebarOpen={this.state.openSidebar}
          />
          <Provider dialog={this.dialogStore}>
            <AntLayout style={{padding: '24px'}}>
              <Dialogs />
              {children}
            </AntLayout>
          </Provider>
        </AntLayout>
      </AntLayout>
    );
  }
}

export default withRouter(App);
