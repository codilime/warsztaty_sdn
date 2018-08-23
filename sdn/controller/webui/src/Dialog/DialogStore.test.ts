/* tslint:disable */
/* global it, describe */
import 'mocha';
import * as chai from 'chai';
import * as sinon from 'sinon';
import * as sinonChai from 'sinon-chai';

import * as Ajax from 'rxjs/observable/dom/ajax';
import {Observable, TestScheduler} from 'rxjs';

import {DialogStore} from './DialogStore';

const should = chai.should();
chai.use(sinonChai);

describe('DialogStore', () => {
  describe('constructor()', () => {
    it('should requires token and serverUrl', () => {
      should.throw(() => {
        new DialogStore();
      }, '[DialogStore]: Api object is required!');
      should.not.throw(() => {
        new DialogStore({});
      }, Error);
    });
  });

  describe('openDialog()', () => {
    let store = undefined;
    const api = {};

    beforeEach(() => {
      store = new DialogStore(api);
      store.dialogs.push({
        additionalProps: {name: 'foo'},
        dialogId: 'fooDialog',
        isInProgress: false,
        isOpen: false,
      });
    });

    afterEach(() => {
      store = undefined;
    });

    it('should open closed dialog', () => {
      store.openDialog('fooDialog', '/test', 'PUT', {name: 'foo'});

      store.dialogs.toJS()[0].should.deep.include({
        additionalProps: {name: 'foo'},
        dialogId: 'fooDialog',
        errorMessage: null,
        isInProgress: false,
        isOpen: true,
        method: 'PUT',
        url: '/test',
      });
    });

    it('should add new dialog to dialog list', () => {
      store.openDialog('barDialog', '/test', 'PUT', {name: 'bar'});

      store.dialogs.toJS()[1].should.deep.include({
        additionalProps: {name: 'bar'},
        dialogId: 'barDialog',
        errorMessage: null,
        isInProgress: false,
        isOpen: true,
        method: 'PUT',
        url: '/test',
      });
    });
  });

  describe('closeDialog()', () => {
    let store = undefined;
    const api = {};

    beforeEach(() => {
      store = new DialogStore(api);
      store.dialogs.push({
        additionalProps: {name: 'foo'},
        dialogId: 'fooDialog',
        errorMessage: null,
        isInProgress: false,
        isOpen: false,
      });
    });

    afterEach(() => {
      store = undefined;
    });

    it('should close opened dialog', () => {
      store.closeDialog('fooDialog');

      store.dialogs.toJS().should.deep.equal([
        {
          additionalProps: {name: 'foo'},
          dialogId: 'fooDialog',
          isInProgress: false,
          errorMessage: null,
          isOpen: false,
        },
      ]);
    });

    it("should throw error when dialog doesn't exist", () => {
      should.throw(
        () => store.closeDialog('barDialog'),
        "[DialogStore]: Dialog 'barDialog' doesn't exit!",
      );
    });
  });

  describe('execute()', async () => {
    let store = undefined;
    const api = {
      executeRequest: sinon.spy(() => new Promise(resolve => resolve(true))),
    };

    beforeEach(() => {
      store = new DialogStore(api);
      sinon.spy(store, 'closeDialog');
      store.dialogs.push(
        {
          additionalProps: {name: 'foo'},
          dialogId: 'fooDialog',
          errorMessage: null,
          isInProgress: false,
          isOpen: true,
          method: 'PUT',
          url: '/test',
        },
        {
          additionalProps: {name: 'bar'},
          dialogId: 'barDialog',
          errorMessage: null,
          isInProgress: false,
          isOpen: false,
          method: 'PUT',
          url: '/test',
        },
        {
          additionalProps: {name: 'baz'},
          dialogId: 'bazDialog',
          errorMessage: null,
          isInProgress: true,
          isOpen: true,
          method: 'PUT',
          url: '/test',
        },
        {
          additionalProps: {name: 'qux'},
          dialogId: 'quxDialog',
          errorMessage: null,
          isInProgress: false,
          isOpen: true,
          method: 'REMOVE',
          url: '/test',
        },
      );
    });

    afterEach(() => {
      store = undefined;
    });

    it('should call executeRequest api method', async () => {
      await store.execute('fooDialog', {id: 'foo'});
      api.executeRequest.should.calledWith('/test', 'PUT', {id: 'foo'});
    });

    it('should resolve promise returned by openDialog method', done => {
      store
        .openDialog('fooDialog', '/test', 'PUT', {name: 'foo'})
        .then(() => done());
      store.execute('fooDialog', {id: 'foo'});
    });

    it('should set error message', async () => {
      api.executeRequest = sinon.spy(
        () => new Promise((resolve, reject) => reject('Sample error')),
      );

      await store.execute('fooDialog', {id: 'foo'});

      store.openedDialogs.should.deep.equal([
        {
          additionalProps: {name: 'foo'},
          dialogId: 'fooDialog',
          errorMessage: 'Sample error',
          isInProgress: false,
          isOpen: true,
          method: 'PUT',
          url: '/test',
        },
        {
          additionalProps: {name: 'baz'},
          dialogId: 'bazDialog',
          errorMessage: null,
          isInProgress: true,
          isOpen: true,
          method: 'PUT',
          url: '/test',
        },
        {
          additionalProps: {name: 'qux'},
          dialogId: 'quxDialog',
          errorMessage: null,
          isInProgress: false,
          isOpen: true,
          method: 'REMOVE',
          url: '/test',
        },
      ]);
    });

    it('should throw error', async () => {
      try {
        await store.execute('bar', {id: 'foo'});
      } catch (error) {
        error.message.should.equal("[DialogStore]: Dialog 'bar' doesn't exit!");
      }

      try {
        await store.execute('barDialog', {id: 'foo'});
      } catch (error) {
        error.message.should.equal(
          "[DialogStore]: Dialog 'barDialog' doesn't open!",
        );
      }

      try {
        await store.execute('bazDialog', {id: 'foo'});
      } catch (error) {
        error.message.should.equal(
          "[DialogStore]: Dialog 'bazDialog' is in progress state!",
        );
      }

      try {
        await store.execute('quxDialog', {id: 'foo'});
      } catch (error) {
        error.message.should.equal(
          "[DialogStore]: 'REMOVE' doesn't valid method type!",
        );
      }
    });
  });

  describe('startProgress()', () => {
    let store = undefined;
    const api = {};

    beforeEach(() => {
      store = new DialogStore(api);
      store.dialogs.push({
        additionalProps: {name: 'foo'},
        dialogId: 'fooDialog',
        isInProgress: false,
        isOpen: true,
      });

      store.dialogs.push({
        additionalProps: {name: 'bar'},
        dialogId: 'barDialog',
        isInProgress: false,
        isOpen: false,
      });
    });

    afterEach(() => {
      store = undefined;
    });

    it('should update isInProgress flag to true', () => {
      store.startProgress('fooDialog');

      store.dialogs.toJS().should.deep.equal([
        {
          additionalProps: {name: 'foo'},
          dialogId: 'fooDialog',
          isInProgress: true,
          isOpen: true,
        },
        {
          additionalProps: {name: 'bar'},
          dialogId: 'barDialog',
          isInProgress: false,
          isOpen: false,
        },
      ]);
    });

    it('should throw error when dialog is closed', () => {
      should.throw(
        () => store.startProgress('barDialog'),
        "[DialogStore]: Dialog 'barDialog' is closed!",
      );
    });

    it("should throw error when dialog doesn't exist", () => {
      should.throw(
        () => store.startProgress('bazDialog'),
        "[DialogStore]: Dialog 'bazDialog' doesn't exit!",
      );
    });
  });

  describe('stopProgress()', () => {
    let store = undefined;
    const api = {};

    beforeEach(() => {
      store = new DialogStore(api);
      store.dialogs.push({
        additionalProps: {name: 'foo'},
        dialogId: 'fooDialog',
        isInProgress: true,
        isOpen: true,
      });

      store.dialogs.push({
        additionalProps: {name: 'bar'},
        dialogId: 'barDialog',
        isInProgress: false,
        isOpen: false,
      });
    });

    afterEach(() => {
      store = undefined;
    });

    it('should update isInProgress flag to true', () => {
      store.stopProgress('fooDialog');

      store.dialogs.toJS().should.deep.equal([
        {
          additionalProps: {name: 'foo'},
          dialogId: 'fooDialog',
          isInProgress: false,
          isOpen: true,
        },
        {
          additionalProps: {name: 'bar'},
          dialogId: 'barDialog',
          isInProgress: false,
          isOpen: false,
        },
      ]);
    });

    it('should throw error when dialog is closed', () => {
      should.throw(
        () => store.stopProgress('barDialog'),
        "[DialogStore]: Dialog 'barDialog' is closed!",
      );
    });

    it("should throw error when dialog doesn't exist", () => {
      should.throw(
        () => store.stopProgress('bazDialog'),
        "[DialogStore]: Dialog 'bazDialog' doesn't exit!",
      );
    });
  });

  describe('get openedDialogs()', () => {
    let store = undefined;
    const api = {};

    beforeEach(() => {
      store = new DialogStore(api);
      store.dialogs.push(
        {
          additionalProps: {name: 'foo'},
          dialogId: 'fooDialog',
          isInProgress: false,
          isOpen: true,
        },
        {
          additionalProps: {name: 'bar'},
          dialogId: 'barDialog',
          isInProgress: false,
          isOpen: false,
        },
      );
    });

    afterEach(() => {
      store = undefined;
    });

    it('should open closed dialog', () => {
      store.openedDialogs.should.deep.equal([
        {
          additionalProps: {name: 'foo'},
          dialogId: 'fooDialog',
          isInProgress: false,
          isOpen: true,
        },
      ]);
    });
  });
});
