import * as React from 'react';
import {Trans, translate} from 'react-i18next';

import {TranslationFunction} from 'i18next';

import {Icon, Layout as AntLayout} from 'antd';

import SidebarMenu from './SidebarMenu';

const {Sider: AntSider} = AntLayout;

import 'antd/lib/layout/style';

import './Sider.less';

interface IProps {
  isSidebarOpen: boolean;
  t?: TranslationFunction;
}
@translate('app')
class Sidebar extends React.Component<IProps> {
  public render(): React.ReactNode {
    return (
      <AntSider className="sider" collapsed={!this.props.isSidebarOpen}>
        <div className="cpe-logo">
          <Icon type="cloud-o" />
          <span className="collapsible">
            <Trans i18nKey="sidebar.title" />
          </span>
        </div>
        <SidebarMenu />
      </AntSider>
    );
  }
}

export default Sidebar;
