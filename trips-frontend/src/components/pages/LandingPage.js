import React from "react";
import tw from "twin.macro"; //eslint-disable-line
import { css } from "styled-components/macro"; //eslint-disable-line

import Hero from "components/cards/HeroWithImage";
import ThreeColSlider from "components/cards/ThreeColSlider";
import TwoTrendingPreviewCardsWithImage from "components/cards/TwoPreviewsWithDescription";
import TwoColSingleFeatureWithStats from "components/cards/StatsWithImage";
import TwoColumnWithImageAndProfilePictureReview from "components/cards/ReviewsWithImage";
import FaqWithSideImage from "components/cards/FaqWithSideImage";

const heroHeading = (
  <>
    Visit amazing places
    <wbr />
    <br />
    <span tw="text-primary-500">Create great memories</span>
  </>
);
const heroDescription =
  "We have been organizing tours around the world for 5 years. We provide great memories and amazing experiences.";
const heroPrimaryActionText = "Sign Up";
const heroSecondaryActionText = "Search Tours";

const LandingPage = () => {
  return (
    <React.Fragment>
      <Hero
        heading={heroHeading}
        description={heroDescription}
        primaryActionUrl="/register"
        primaryActionText={heroPrimaryActionText}
        secondaryActionUrl={"/tours"}
        secondaryActionText={heroSecondaryActionText}
      />
      <ThreeColSlider />
      <TwoTrendingPreviewCardsWithImage />
      <TwoColSingleFeatureWithStats />
      <TwoColumnWithImageAndProfilePictureReview textOnLeft={true} />
      <FaqWithSideImage />
    </React.Fragment>
  );
};

export default LandingPage;
