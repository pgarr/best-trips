import React from "react";
import { withRouter } from "react-router-dom";
import tw from "twin.macro";

import "tailwindcss/dist/base.css";
import RoutesList from "./RoutesList";

const StyledDiv = tw.div`font-display min-h-screen text-secondary-500 p-8 overflow-hidden`;

const App = () => {
  return (
    <StyledDiv>
      <RoutesList />
    </StyledDiv>
  );
};

export default withRouter(App);
