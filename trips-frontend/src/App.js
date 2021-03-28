import React from "react";
import tw from "twin.macro";

import "tailwindcss/dist/base.css";
import LandingPage from "pages/LandingPage";

const StyledDiv = tw.div`font-display min-h-screen text-secondary-500 p-8 overflow-hidden`;

const App = () => {
  return (
    <StyledDiv>
      <LandingPage />
    </StyledDiv>
  );
};

export default App;
