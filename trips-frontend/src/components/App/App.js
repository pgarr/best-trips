import React from "react";
import { withRouter } from "react-router-dom";
import "tailwindcss/dist/base.css";
import LayoutWrapper from "./LayoutWrapper";

import RoutesList from "./RoutesList";

const App = () => {
  return (
    <LayoutWrapper>
      <RoutesList />
    </LayoutWrapper>
  );
};

export default withRouter(App);
