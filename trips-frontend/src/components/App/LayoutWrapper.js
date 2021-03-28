import Footer from "components/footers/Footer";
import React from "react";
import tw from "twin.macro";

const StyledDiv = tw.div`font-display min-h-screen text-secondary-500 p-8 overflow-hidden`;

const LayoutWrapper = ({ children }) => {
  return (
    <StyledDiv>
      {children}
      <Footer />
    </StyledDiv>
  );
};

export default LayoutWrapper;
