import * as React from 'react';

import {Icon as AntIcon, Menu as AntMenu} from 'antd';
import {i18n as I18n} from 'i18next';
import {Trans, translate} from 'react-i18next';

import 'antd/lib/icon/style';
import 'antd/lib/menu/style';

interface IProps {
  onToggleSidebar: () => void;
  userName?: string;
  openSidebar?: boolean;
  i18n?: I18n;
}
@translate('app')
export default class Navbar extends React.Component<IProps> {
  public render(): React.ReactNode {
    return (
      <AntMenu
        mode="horizontal"
        selectable={false}
        theme="light"
        className="navbar-header"
      >
        <AntMenu.Item className="no-padding">
          <AntIcon
            onClick={this.props.onToggleSidebar}
            type={`menu-${this.props.openSidebar ? 'fold' : 'unfold'}`}
            className="toggle-sidebar-icon"
          />
        </AntMenu.Item>
      </AntMenu>
    );
  }
}
