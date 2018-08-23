/* tslint:disable */
/* global it, describe */
import 'mocha';
import * as chai from 'chai';
import * as sinonChai from 'sinon-chai';

import globalMessageStore, {GlobalMessageStore} from './GlobalMessageStore';

const should = chai.should();
chai.use(sinonChai);

describe('GlobalMessageStore', () => {
  describe('push()', () => {
    it('should push message correct', () => {
      const store = new GlobalMessageStore();

      store.push('Test error', 'error');
      store.push('Test error 2', 'error');
      store.push('Test error 3');

      store.messages[0].should.deep.equal({
        id: 0,
        message: 'Test error',
        show: true,
        type: 'error',
      });
      store.messages[1].should.deep.equal({
        id: 1,
        message: 'Test error 2',
        show: true,
        type: 'error',
      });
      store.messages[2].should.deep.equal({
        id: 2,
        message: 'Test error 3',
        show: true,
        type: 'info',
      });
    });
  });

  describe('push()', () => {
    it('should hide message correct', () => {
      const store = new GlobalMessageStore();

      store.push('Test error', 'error');
      store.push('Test error 2', 'error');

      store.remove(0);

      store.messages[0].should.deep.equal({
        id: 0,
        message: 'Test error',
        show: false,
        type: 'error',
      });
      store.messages[1].should.deep.equal({
        id: 1,
        message: 'Test error 2',
        show: true,
        type: 'error',
      });
    });
    it('should throw error when id is wrong', () => {
      const store = new GlobalMessageStore();

      should.throw(
        () => {
          store.remove(12);
        },
        Error,
        '[GlobalMessageStore.remove] 12 is wrong message id!',
      );
    });
  });
});

describe('globalMessageStore', () => {
  it('should be a GlobalMessageStore member', () => {
    globalMessageStore.constructor.should.deep.equal(GlobalMessageStore);
  });
});
