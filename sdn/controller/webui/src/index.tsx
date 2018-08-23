import createHashHistory from 'history/createHashHistory';
import {Provider} from 'mobx-react';
import * as React from 'react';
import {render} from 'react-dom';
import * as Loadable from 'react-loadable';

import './i18n';

import ConfigStore from './config/ConfigStore';

import LoadingIndicator from './components/LoadingIndicator';
import {ConfigApi} from './config/ConfigApi';

const configApi = new ConfigApi();
const configStore = new ConfigStore(configApi);

const hashHistory = createHashHistory();

configStore.fetch().then(() => {
  const Test = Loadable({
    loader: () => import(/* webpackChunkName: "Root" */ './App/Root'),
    loading: LoadingIndicator,
    render(loaded, props) {
      const Component = loaded.default;

      return (
        <Provider config={configStore}>
          <Component {...props} />
        </Provider>
      );
    },
  });
  render(<Test history={hashHistory} />, document.getElementById('root'));
});
