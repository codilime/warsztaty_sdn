import {BaseApi, TFetchResponse} from './';

import {parse as parseSearchQuery, stringify as stringifySearchQuery} from 'qs';

import {ICollectionApi} from './ICollectionApi';
import {TSchema} from './TSchema';

export class CollectionApi extends BaseApi implements ICollectionApi {
  private schema: TSchema;

  constructor(options, schema) {
    super(options);

    this.schema = schema;
  }

  public fetchCollection(search, headers?) {
    return new Promise<TFetchResponse>((resolve, reject) => {
      this.fetch(
        this.schema.url,
        headers,
      ).subscribe(
        (data: TFetchResponse) => {
          resolve(data);
        },
        (error: Error) => {
          reject(error);
        },
      );
    });
  }
}
