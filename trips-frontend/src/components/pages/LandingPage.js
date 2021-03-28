import React from "react";

import Hero from "components/cards/HeroWithImage";
import ThreeColSlider from "components/cards/ThreeColSlider";
import TwoTrendingPreviewCardsWithImage from "components/cards/TwoPreviewsWithDescription";
import TwoColSingleFeatureWithStats from "components/cards/StatsWithImage";
import TwoColumnWithImageAndProfilePictureReview from "components/cards/ReviewsWithImage";
import FaqWithSideImage from "components/cards/FaqWithSideImage";

const LandingPage = () => {
  return (
    <React.Fragment>
      <Hero />
      <ThreeColSlider />
      <TwoTrendingPreviewCardsWithImage />
      <TwoColSingleFeatureWithStats />
      <TwoColumnWithImageAndProfilePictureReview textOnLeft={true} />
      <FaqWithSideImage />
    </React.Fragment>
  );
};

export default LandingPage;
