import {cloneDeep} from 'lodash';

let i18n;

export function setI18n(instance) {
  i18n = instance;
}

export const TranslateSchema = {
  type: '3rdParty',

  init(instance) {
    setI18n(instance);
  },
};

export async function schemaTranslate(
  schema: any,
  ns: string,
  prefix: string = 'dialog',
) {
  if (i18n.isInitialized) {
    const t = i18n.getFixedT(null, ns);
    const result = cloneDeep(schema);

    if (schema.title) {
      const title = t(`${prefix}.title`);
      result.title = title === `${prefix}.title` ? schema.title : title;
    }

    if (schema.description) {
      const description = t(`${prefix}.description`);
      result.description =
        description === `${prefix}.description`
          ? schema.description
          : description;
    }

    if (schema.type.includes('object')) {
      for (const key of Object.keys(schema.properties)) {
        result.properties[key] = await schemaTranslate(
          schema.properties[key],
          ns,
          `${prefix}.${key}`,
        );
      }
    }

    return result;
  }
  i18n.on('initialized', async () => {
    return await schemaTranslate(schema, ns);
  });
}
