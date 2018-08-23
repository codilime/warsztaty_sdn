/* tslint:disable */
/* global it, describe */
import 'mocha';
import * as chai from 'chai';
import * as sinon from 'sinon';
import * as sinonChai from 'sinon-chai';

import * as Ajax from 'rxjs/observable/dom/ajax';
import {Observable, TestScheduler} from 'rxjs';

import {BaseStore} from './BaseStore';

const should = chai.should();
chai.use(sinonChai);

describe('BaseStore', () => {
  describe('constructor()', () => {
    it('should requires token and serverUrl', () => {
      should.throw(() => {
        new BaseStore();
      }, Error);

      should.not.throw(() => {
        new BaseStore({});
      }, Error);
    });
  });

  describe('get isLoading()', () => {
    it('should returns true as loading state', () => {
      const baseStore = new BaseStore({});

      baseStore.isLoading.should.be.true;
    });
  });

  describe('stopPolling()', () => {
    it('should stops polling stream');
  });

  describe('startPolling()', () => {
    it('should starts polling stream');
  });

  describe('fetch()', () => {
    it('should exist', () => {
      const baseStore = new BaseStore({});

      baseStore.fetch.should.exist;
    });

    it('should throw error', () => {
      const baseStore = new BaseStore({});

      should.throw(baseStore.fetch, Error);
    });
  });
});
