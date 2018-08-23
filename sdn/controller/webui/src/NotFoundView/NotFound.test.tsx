/* global it, describe */
import 'mocha';
import * as chai from 'chai';
import * as sinon from 'sinon';
import * as sinonChai from 'sinon-chai';
import * as chaiEnzyme from 'chai-enzyme';

import {shallow} from 'enzyme';
import * as React from 'react';

import {NotFound} from './NotFound';

chai.use(chaiEnzyme());
chai.use(sinonChai);
chai.should();

const sandbox = sinon.createSandbox();

describe('< NotFound />', () => {
  it('should exist', () => {
    const wrapper = shallow(<NotFound />);

    wrapper.should.not.equal(undefined);
  });

  it('should match snapshot', () => {
    const wrapper = shallow(<NotFound />);
    wrapper.should.to.matchSnapshot();
  });
});
