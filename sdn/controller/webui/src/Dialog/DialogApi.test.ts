/* tslint:disable */
/* global it, describe */
import 'mocha';
import * as chai from 'chai';
import * as sinon from 'sinon';
import * as sinonChai from 'sinon-chai';
import {Observable} from 'rxjs';

import {DialogApi} from './DialogApi';

chai.should();
chai.use(sinonChai);

describe('DialogApi', () => {
  describe('executeRequest()', () => {
    let api = undefined;

    afterEach(() => {
      api.ajax.restore();
      api = undefined;
    });

    it('should return true as success, data with id', async () => {
      api = new DialogApi({
        token: 'testToken',
        serverUrl: 'http://test.com',
      });

      sinon.stub(api, 'ajax').callsFake(() =>
        Observable.of({
          totalCount: 1,
          payload: [{name: 'test'}],
        }),
      );
      const data = await api.executeRequest('/v1.0/test', 'PUT', {
        id: 'testId',
      });

      data.should.equal(true);
      api.ajax.should.calledWith('/v1.0/test/testId', 'PUT', {id: 'testId'});
    });

    it('should return true as success, data without id', async () => {
      api = new DialogApi({
        token: 'testToken',
        serverUrl: 'http://test.com',
      });

      sinon.stub(api, 'ajax').callsFake(() =>
        Observable.of({
          totalCount: 1,
          payload: [{name: 'test'}],
        }),
      );
      const data = await api.executeRequest('/v1.0/test', 'PUT', {});

      data.should.equal(true);
      api.ajax.should.calledWith('/v1.0/test/', 'PUT', {});
    });

    it('should returns HTTP error', async () => {
      api = new DialogApi({
        token: 'testToken',
        serverUrl: 'http://test.com',
      });

      sinon.stub(api, 'ajax').callsFake(() => {
        return Observable.throw('Test error');
      });
      try {
        await api.executeRequest('/v1.0/test', 'PUT', {});
      } catch (error) {
        error.should.equal('Test error');
      }
    });
  });
});
