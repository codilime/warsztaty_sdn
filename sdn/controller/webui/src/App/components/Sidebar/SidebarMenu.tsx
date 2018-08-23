import * as React from 'react';
import {Trans, translate} from 'react-i18next';
import {RouteComponentProps} from 'react-router';
import {Link, withRouter} from 'react-router-dom';

import {Icon as AntIcon, Menu as AntMenu} from 'antd';
import 'antd/lib/icon/style';
import 'antd/lib/menu/style';

const routes = [
  {
    icon: 'cloud',
    i18nKey: 'containers',
    url: '/containers',
  },
  {
    icon: 'share-alt',
    i18nKey: 'networks',
    url: '/networks',
  },
  {
    icon: 'pushpin-o',
    i18nKey: 'logical_ports',
    url: '/logical_ports',
  },
];

interface IProps extends RouteComponentProps<{}> {}

@translate('app')
export class SidebarMenu extends React.Component<IProps> {
  public render(): React.ReactNode {
    const selectedKeys = routes.reduce((result, route) => {
      if (this.props.location.pathname === '/') {
        result = ['/'];
      } else if (
        route.url !== '/' &&
        this.props.location.pathname.startsWith(route.url)
      ) {
        result.push(route.url);
      }

      return result;
    }, []);

    return (
      <AntMenu theme={'dark'} selectedKeys={selectedKeys}>
        {routes.map(route => (
          <AntMenu.Item key={route.url}>
            <Link to={route.url}>
              <AntIcon type={route.icon} />
              <span>
                <Trans i18nKey={`sidebar.menu.${route.i18nKey}`} />
              </span>
            </Link>
          </AntMenu.Item>
        ))}
      </AntMenu>
    );
  }
}

export default withRouter(SidebarMenu);
