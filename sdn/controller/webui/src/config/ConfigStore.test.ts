/* global it, describe */
import * as chai from 'chai';
import 'mocha';
import * as sinon from 'sinon';
import * as sinonChai from 'sinon-chai';

import ConfigStore from './ConfigStore';

const should = chai.should();

chai.use(sinonChai);

describe('ConfigStore', () => {
  describe('constructor()', () => {
    it('should requires token and serverUrl', () => {
      should.throw(() => {
        new ConfigStore();
      }, Error);

      should.not.throw(() => {
        new ConfigStore({});
      }, Error);
    });
  });
  describe('fetch()', () => {
    it('should exist', () => {
      const store = new ConfigStore({});

      store.fetch.should.exist;
    });

    it('should call api.fetch()', async () => {
      const api = {
        fetch: sinon.spy(
          () =>
            new Promise(resolve =>
              resolve({
                payload: {},
              }),
            ),
        ),
      };

      const store = new ConfigStore(api);

      await store.fetch();

      api.fetch.should.callCount(1);
    });

    it('should handle error message', async () => {
      const api = {
        fetch: () =>
          new Promise((resolve, reject) => reject('TEST ERROR MESSAGE')),
      };

      const store = new ConfigStore(api);

      try {
        await store.fetch();
      } catch (error) {
        should.exist(error);
        error.should.be.an
          .instanceOf(Error)
          .with.property('message', '[ConfigStore]: TEST ERROR MESSAGE');
      }
    });
  });
});
