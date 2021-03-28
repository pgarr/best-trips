import React from "react";
import { withRouter } from "react-router-dom";
import "tailwindcss/dist/base.css";
import LayoutWrapper from "./LayoutWrapper";

import RoutesSwitch from "./RoutesSwitch";

const App = () => {
  return (
    <LayoutWrapper>
      <RoutesSwitch />
    </LayoutWrapper>
  );
};

export default withRouter(App);
