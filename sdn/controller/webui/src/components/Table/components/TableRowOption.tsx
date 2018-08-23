import * as React from 'react';

import {Icon as AntIcon} from 'antd';

import 'antd/lib/icon/style';

interface IProps {
  type: string;
  onClick: () => void;
}

const TableRowOption = ({type, onClick}: IProps): JSX.Element => (
  <a onClick={onClick}>
    <AntIcon type={type} />
  </a>
);

export default TableRowOption;
