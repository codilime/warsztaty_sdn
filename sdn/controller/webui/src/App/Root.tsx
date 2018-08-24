import * as H from 'history';
import {Provider} from 'mobx-react';
import * as React from 'react';
import * as Loadable from 'react-loadable';
import {Route, Router, Switch} from 'react-router-dom';

import {IConfigStore} from '../config/IConfigStore';

import GlobalMessage from '../GlobalMessage';
import LoadingIndicator from './../components/LoadingIndicator';
import App from './App';

import './Root.less';

interface IProps {
  config: IConfigStore;
  history: H.History;
}

export class Root extends React.Component<IProps> {
  public render() {
    const {history} = this.props;

    return (
      <Provider>
        <Router history={history}>
          <div className={'cpe-app'}>
            <GlobalMessage />
            <App>
              <Switch>
                <Route
                  exact={true}
                  strict={true}
                  path="/"
                  component={Loadable({
                    loader: () =>
                      import(/* webpackChunkName: "home" */ '../Home'),
                    loading: LoadingIndicator,
                  })}
                />
                <Route
                  exact={true}
                  strict={true}
                  path="/containers"
                  component={Loadable({
                    loader: () =>
                      import(/* webpackChunkName: "containers" */ '../Containers'),
                    loading: LoadingIndicator,
                  })}
                />
                <Route
                  exact={true}
                  strict={true}
                  path="/networks"
                  component={Loadable({
                    loader: () =>
                      import(/* webpackChunkName: "networks" */ '../Networks'),
                    loading: LoadingIndicator,
                  })}
                />
                <Route
                  exact={true}
                  strict={true}
                  path="/logical_ports"
                  component={Loadable({
                    loader: () =>
                      import(/* webpackChunkName: "logicalPorts" */ './../LogicalPorts'),
                    loading: LoadingIndicator,
                  })}
                />
                <Route
                  component={Loadable({
                    loader: () =>
                      import(/* webpackChunkName: "NotFound" */ './../NotFoundView'),
                    loading: LoadingIndicator,
                  })}
                />
              </Switch>
            </App>
          </div>
        </Router>
      </Provider>
    );
  }
}

export default Root;
