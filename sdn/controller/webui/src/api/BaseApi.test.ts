/* tslint:disable */
/* global it, describe */
import 'mocha';
import * as chai from 'chai';
import * as sinon from 'sinon';
import * as sinonChai from 'sinon-chai';

import * as Ajax from 'rxjs/observable/dom/ajax';
import {Observable, TestScheduler} from 'rxjs';

import {BaseApi} from './BaseApi';

const should = chai.should();
chai.use(sinonChai);

describe('BaseApi', () => {
  describe('static parseXHRError()', () => {
    it("should return 'Unknown error!' message", () => {
      BaseApi.parseXHRError().should.equal('Unknown error!');
      BaseApi.parseXHRError({data: 'Test error!'}).should.equal(
        'Unknown error!',
      );
      BaseApi.parseXHRError({xhr: {}}).should.equal('Unknown error!');
      BaseApi.parseXHRError({xhr: {response: 123}}).should.equal(
        'Unknown error!',
      );
      BaseApi.parseXHRError({xhr: {response: {}}}).should.equal(
        'Unknown error!',
      );
      BaseApi.parseXHRError({xhr: {response: {error: 12}}}).should.equal(
        'Unknown error!',
      );
      BaseApi.parseXHRError({xhr: {response: {error: {}}}}).should.equal(
        'Unknown error!',
      );
      BaseApi.parseXHRError({
        xhr: {response: {error: {message: 123}}},
      }).should.equal('Unknown error!');
    });

    it('should return correct error message', () => {
      BaseApi.parseXHRError({message: 'Test error!'}).should.equal(
        'Test error!',
      );
    });

    it('should return error message from xhr object', () => {
      BaseApi.parseXHRError({xhr: {response: 'Error!'}}).should.equal('Error!');
      BaseApi.parseXHRError({xhr: {response: {error: 'Error!'}}}).should.equal(
        'Error!',
      );
      BaseApi.parseXHRError({
        xhr: {response: {error: {message: 'Error!'}}},
      }).should.equal('Error!');
    });
  });

  describe('constructor()', () => {
    it('should requires token and serverUrl', () => {
      should.throw(() => {
        new BaseApi({});
      }, Error);
      should.throw(() => {
        new BaseApi({token: 'test token'});
      }, Error);
      should.throw(() => {
        new BaseApi({serverUrl: 'http://url.test'});
      }, Error);
      should.not.throw(() => {
        new BaseApi({
          token: 'test token',
          serverUrl: 'http://url.test',
        });
      }, Error);
    });
  });

  describe('fetch()', () => {
    let testScheduler;

    beforeEach(() => {
      testScheduler = new TestScheduler((a, b) => a.should.deep.equal(b));
    });

    afterEach(() => {
      Ajax.ajax.restore();
    });

    it('should return stream with correct data', () => {
      sinon.stub(Ajax, 'ajax').callsFake(urlOrRequest =>
        Observable.of({
          response: [{name: 'vader'}],
        }),
      );

      testScheduler.schedule(() => {
        const api = new BaseApi({
          token: 'testToken',
          serverUrl: 'http://test.com',
        });

        testScheduler.expectObservable(api.fetch('/test/url')).toBe('-(a|)', {
          a: {
            payload: [{name: 'vader'}],
          },
        });
      }, 10);
      testScheduler.flush();
    });

    it('should return error message', () => {
      sinon.stub(Ajax, 'ajax').callsFake(() => Observable.throw({}));
      testScheduler.schedule(() => {
        const api = new BaseApi({
          token: 'testToken',
          serverUrl: 'http://test.com',
        });

        testScheduler
          .expectObservable(api.fetch('/test/url'))
          .toBe('-#', null, 'Unknown error!');
      }, 10);
      testScheduler.flush();
    });
  });

  describe('ajax()', () => {
    let testScheduler;

    beforeEach(() => {
      testScheduler = new TestScheduler((a, b) => a.should.deep.equal(b));
    });

    afterEach(() => {
      Ajax.ajax.restore();
    });

    it('should return stream with value', () => {
      sinon.stub(Ajax, 'ajax').callsFake(urlOrRequest => {
        urlOrRequest.body.should.deep.equal({});
        urlOrRequest.method.should.equal('POST');
        urlOrRequest.headers.should.deep.equal({
          Accept: 'application/json',
          'Content-Type': 'application/json',
          'X-Auth-Token': 'testToken',
        });
        return Observable.of({
          response: null,
        });
      });

      testScheduler.schedule(() => {
        const api = new BaseApi({
          token: 'testToken',
          serverUrl: 'http://test.com',
        });

        testScheduler
          .expectObservable(api.ajax('/test/url', 'POST', {}))
          .toBe('-(a|)', {
            a: null,
          });
      }, 10);
      testScheduler.flush();
    });

    it('should return stream with value (optional headers)', () => {
      sinon.stub(Ajax, 'ajax').callsFake(urlOrRequest => {
        urlOrRequest.body.should.deep.equal({});
        urlOrRequest.method.should.equal('POST');
        urlOrRequest.headers.should.deep.equal({
          Accept: 'application/text',
          'Content-Type': 'application/json',
          'X-Auth-Token': 'testToken',
        });
        return Observable.of({
          response: null,
        });
      });

      testScheduler.schedule(() => {
        const api = new BaseApi({
          token: 'testToken',
          serverUrl: 'http://test.com',
        });

        testScheduler
          .expectObservable(
            api.ajax('/test/url', 'POST', {}, {Accept: 'application/text'}),
          )
          .toBe('-(a|)', {
            a: null,
          });
      }, 10);
      testScheduler.flush();
    });

    it('should return error message', () => {
      sinon.stub(Ajax, 'ajax').callsFake(() => Observable.throw({}));
      testScheduler.schedule(() => {
        const api = new BaseApi({
          token: 'testToken',
          serverUrl: 'http://test.com',
        });

        testScheduler
          .expectObservable(api.ajax('/test/url', 'POST', {}))
          .toBe('-#', null, 'Unknown error!');
      }, 10);
      testScheduler.flush();
    });
  });
});
