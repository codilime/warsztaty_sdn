import * as React from 'react';

import {Table as AntTable} from 'antd';

import {TableProps} from 'antd/lib/table/interface';
import 'antd/lib/table/style';

import './styles.less';

const Table = ({
  dataSource = [],
  columns = [],
  pagination = false,
  rowKey = (d, i) => d.id || i.toString(),
}: TableProps<any>) => (
  <AntTable
    columns={columns}
    dataSource={dataSource}
    pagination={pagination}
    rowKey={rowKey}
  />
);

export default Table;
