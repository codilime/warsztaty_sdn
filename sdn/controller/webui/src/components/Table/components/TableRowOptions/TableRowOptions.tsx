import * as React from 'react';

import {Icon as AntIcon} from 'antd';

import 'antd/lib/icon/style';

import './styles.less';

interface IProps {
  children: JSX.Element | JSX.Element[];
}

const TableRowOptions = ({children}: IProps): JSX.Element => (
  <div className="options">{children}</div>
);

export default TableRowOptions;
