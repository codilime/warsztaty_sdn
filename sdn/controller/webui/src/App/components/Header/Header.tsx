import * as React from 'react';

import {Layout as AntLayout} from 'antd';

import Navbar from './Navbar';

import 'antd/lib/layout/style';

import './Header.less';

const {Header: AntHeader} = AntLayout;

interface IProps {
  isSidebarOpen?: boolean;
  onToggleSidebar: () => void;
}

export default class Header extends React.Component<IProps> {
  public render() {
    return (
      <AntHeader className={'fit-navbar'}>
        <Navbar
          onToggleSidebar={this.props.onToggleSidebar}
          openSidebar={this.props.isSidebarOpen}
        />
      </AntHeader>
    );
  }
}
