import * as i18n from 'i18next';
import * as LanguageDetector from 'i18next-browser-languagedetector';
import * as Backend from 'i18next-xhr-backend';
import {reactI18nextModule} from 'react-i18next';

import {TranslateSchema} from './Dialog/TranslateSchema';

i18n
  .use(Backend)
  .use(LanguageDetector)
  .use(reactI18nextModule)
  .use(TranslateSchema)
  .init({
    fallbackLng: 'en',

    // have a common namespace used around the full app
    ns: ['app'],
    defaultNS: 'translations',

    debug: true,

    interpolation: {
      escapeValue: false, // not needed for react!!
    },

    react: {
      wait: true,
    },
  });
