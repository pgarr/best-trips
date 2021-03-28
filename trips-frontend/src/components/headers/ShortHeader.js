import React from "react";
import tw from "twin.macro";
import styled from "styled-components";
import { css } from "styled-components/macro"; //eslint-disable-line

import Header, {
  LogoLink,
  NavLinks,
  NavLink as NavLinkBase,
} from "./BaseHeader.js";

const StyledHeader = styled(Header)`
  ${tw`justify-between`}
  ${LogoLink} {
    ${tw`mr-8 pb-0`}
  }
`;

const NavLink = tw(NavLinkBase)`
  sm:text-sm sm:mx-6
`;

const navLinks = [
  <NavLinks key={1}>
    <NavLink href="/about">About</NavLink>
    <NavLink href="/login">Login</NavLink>
  </NavLinks>,
];

const ShortHeader = () => {
  return <StyledHeader links={navLinks} collapseBreakpointClass="sm" />;
};

export default ShortHeader;
