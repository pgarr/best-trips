import React from "react";
import { Route, Switch, Redirect } from "react-router-dom";

import LandingPage from "pages/LandingPage";

const RoutesList = () => {
  return (
    <Switch>
      <Route path="/" exact component={LandingPage} />
      <Redirect to="/" />
    </Switch>
  );
};

export default RoutesList;
