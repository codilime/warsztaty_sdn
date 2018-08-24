import {Card} from 'antd';
import * as React from 'react';
import {Trans, translate} from 'react-i18next';

import 'antd/lib/card/style';

export const Home = () => (
  <Card>
    <h2>
      <Trans i18nKey="title" />
    </h2>
    <p>
      <img style={{width: 400}} src={require('./../../css/codilime-logo.png')}/>
    </p>
  </Card>
);

export default translate('home')(Home);
