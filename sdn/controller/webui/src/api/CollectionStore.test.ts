/* global it, describe */
import * as chai from 'chai';
import 'mocha';
import * as sinon from 'sinon';
import * as sinonChai from 'sinon-chai';

import {CollectionStore} from './';
const should = chai.should();

chai.use(sinonChai);

describe('CollectionStore', () => {
  describe('fetch()', () => {
    const dialogStore = {
      startProgress: () => {},
      stopProgress: () => {},
    };

    it('should exist', () => {
      const store = new CollectionStore({}, dialogStore);

      store.fetch.should.exist;
    });

    it('should call api fetchCollection()', async () => {
      const api = {
        fetchCollection: sinon.spy(
          () =>
            new Promise(resolve =>
              resolve({
                payload: [{}],
                totalCount: 1,
              }),
            ),
        ),
      };
      const store = new CollectionStore(api, dialogStore);

      await store.fetch();

      api.fetchCollection.should.callCount(1);
    });

    it('should handle response data correct', async () => {
      const api = {
        fetchCollection: sinon.spy(
          () =>
            new Promise(resolve =>
              resolve({
                payload: [{}],
                totalCount: 1,
              }),
            ),
        ),
      };
      const store = new CollectionStore(api, dialogStore);

      await store.fetch();

      store.data.toJS().should.deep.equal([{}]);
      store.totalCount.should.equal(1);
      store.loadingState.should.equal(false);
    });

    it('should handle error message', async () => {
      const api = {
        fetchCollection: () =>
          new Promise((resolve, reject) => reject('TEST ERROR MESSAGE')),
      };
      const store = new CollectionStore(api, dialogStore);

      await store.fetch();

      store.errorMessage.should.equal('TEST ERROR MESSAGE');
    });
  });
});
