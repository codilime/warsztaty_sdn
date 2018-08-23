/* tslint:disable */
/* global it, describe */
import 'mocha';
import * as chai from 'chai';
import * as sinon from 'sinon';
import * as sinonChai from 'sinon-chai';

import * as Ajax from 'rxjs/observable/dom/ajax';
import {Observable} from 'rxjs';

import {BaseApi} from '../api';
import {ConfigApi} from './ConfigApi';

chai.should();
chai.use(sinonChai);

describe('ConfigApi', () => {
  describe('fetch()', () => {
    beforeEach(() => {
      sinon.stub(BaseApi, 'parseXHRError').returns('sample test error');
    });

    afterEach(() => {
      BaseApi.parseXHRError.restore();
      Ajax.ajax.restore();
    });

    it('should return correct data', async () => {
      sinon.stub(Ajax, 'ajax').callsFake(() =>
        Observable.of({
          response: {
            serverUrl: 'localhost',
          },
        }),
      );

      const api = new ConfigApi();
      const config = await api.fetch();

      config.should.deep.equal({
        serverUrl: 'localhost',
      });
    });

    it('should return correct data (__HOST__)', async () => {
      sinon.stub(Ajax, 'ajax').callsFake(() =>
        Observable.of({
          response: {
            serverUrl: '__HOST__:5321',
          },
        }),
      );

      const api = new ConfigApi();
      const config = await api.fetch();

      config.should.deep.equal({
        serverUrl: 'localhost:5321',
      });
    });

    it('should throw error', async () => {
      sinon.stub(Ajax, 'ajax').callsFake(() => Observable.throw({}));

      const api = new ConfigApi();

      try {
        await api.fetch();
      } catch (error) {
        error.should.equal('sample test error');
      }
    });
  });
});
