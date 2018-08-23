/* tslint:disable */
/* global it, describe */
import 'mocha';
import * as chai from 'chai';
import * as sinon from 'sinon';
import * as sinonChai from 'sinon-chai';
import {Observable} from 'rxjs';

import {CollectionApi} from './';

chai.should();
chai.use(sinonChai);

describe('CollectionApi', () => {
  describe('fetchCollection()', () => {
    let api = undefined;

    afterEach(() => {
      api.fetch.restore();
      api = undefined;
    });

    it('should return correct data', async () => {
      api = new CollectionApi(
        {
          token: 'testToken',
          serverUrl: 'http://test.com',
        },
        {url: '/v1.0/controllers'},
      );

      sinon.stub(api, 'fetch').callsFake(url => {
        switch (url) {
          case '/v1.0/controllers':
            return Observable.of({
              totalCount: 1,
              payload: [{name: 'test'}],
            });
          default:
            return Observable.throw('Test error');
        }
      });
      const data = await api.fetchCollection();

      data.should.deep.equal({
        totalCount: 1,
        payload: [{name: 'test'}],
      });
    });

    it('should returns HTTP error', async () => {
      api = new CollectionApi(
        {
          token: 'testToken',
          serverUrl: 'http://test.com',
        },
        {url: '/v1.0/controllers'},
      );

      sinon.stub(api, 'fetch').callsFake(() => {
        return Observable.throw('Test error');
      });
      try {
        await api.fetchCollection();
      } catch (error) {
        error.should.equal('Test error');
      }
    });
  });
});
