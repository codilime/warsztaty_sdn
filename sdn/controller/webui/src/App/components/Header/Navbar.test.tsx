/* global it, describe */
import * as chai from 'chai';
import * as chaiEnzyme from 'chai-enzyme';
import * as spies from 'chai-spies';
import {shallow} from 'enzyme';
import * as React from 'react';

import Navbar from './Navbar';

chai.use(spies);
chai.use(chaiEnzyme());
chai.should();

describe('< Navbar />', () => {
  it('should exist', () => {
    const wrapper = shallow(
      <Navbar
        activeProject="demo"
        userName="admin"
        onRequestLogout={() => {}} // tslint:disable-line
        onToggleSidebar={() => {}} // tslint:disable-line
      />,
    );

    wrapper.should.not.equal(undefined);
  });
});
