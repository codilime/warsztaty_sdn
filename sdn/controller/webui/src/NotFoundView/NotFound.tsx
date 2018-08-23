import {Card} from 'antd';
import * as React from 'react';
import {Trans, translate} from 'react-i18next';

import 'antd/lib/card/style';

export const NotFound = () => (
  <Card>
    <h2>
      <Trans i18nKey="title" />
    </h2>
    <p>
      <Trans i18nKey="description" />
    </p>
  </Card>
);

export default translate('notFound')(NotFound);
