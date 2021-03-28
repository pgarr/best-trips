import React from "react";
import { Route, Switch, Redirect } from "react-router-dom";

import LandingPage from "components/pages/LandingPage";

const RoutesSwitch = () => {
  return (
    <Switch>
      <Route path="/" exact component={LandingPage} />
      <Redirect to="/" />
    </Switch>
  );
};

export default RoutesSwitch;
