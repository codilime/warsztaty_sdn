import * as React from 'react';

import GlobalMessage from './GlobalMessage';
import globalMessageStore from './GlobalMessageStore';

export default () => <GlobalMessage globalMessageStore={globalMessageStore} />;
export {globalMessageStore};
