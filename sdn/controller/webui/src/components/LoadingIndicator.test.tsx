/* global it, describe */
import * as chai from 'chai';
import * as chaiEnzyme from 'chai-enzyme';
import {shallow} from 'enzyme';
import * as React from 'react';

import LoadingIndicator from './LoadingIndicator';

chai.use(chaiEnzyme());
chai.should();

describe('< LoadingIndicator />', () => {
  it('should exist', () => {
    const wrapper = shallow(<LoadingIndicator />);

    wrapper.should.not.equal(undefined);
  });

  it('should match snapshot', () => {
    const wrapper = shallow(<LoadingIndicator />);
    wrapper.should.to.matchSnapshot();
  });
});
