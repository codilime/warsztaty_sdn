import * as React from 'react';

import {Spin as AntSpin} from 'antd';
import 'antd/lib/spin/style';

export const LoadingIndicator = () => (
  <div className="loading-container" style={{textAlign: 'center'}}>
    <AntSpin spinning={true} size={'large'} />
  </div>
);

export default LoadingIndicator;
