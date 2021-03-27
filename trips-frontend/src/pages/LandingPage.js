import React from 'react';
import tw from 'twin.macro';

import Hero from 'components/cards/HeroWithImage';
import ThreeColSlider from 'components/cards/ThreeColSlider';
import TwoTrendingPreviewCardsWithImage from 'components/cards/TwoPreviewsWithDescription';
import TwoColSingleFeatureWithStats from 'components/cards/StatsWithImage';
import TwoColumnWithImageAndProfilePictureReview from 'components/cards/ReviewsWithImage';
import FaqWithSideImage from 'components/cards/FaqWithSideImage';
import FiveColumnWithInputForm from 'components/footers/FiveColumnWithInputForm';

const StyledDiv = tw.div`font-display min-h-screen text-secondary-500 p-8 overflow-hidden`;

const LandingPage = () => {
  return (
    <StyledDiv className='App'>
      <Hero />
      <ThreeColSlider />
      <TwoTrendingPreviewCardsWithImage />
      <TwoColSingleFeatureWithStats />
      <TwoColumnWithImageAndProfilePictureReview textOnLeft={true} />
      <FaqWithSideImage />
      <FiveColumnWithInputForm />
    </StyledDiv>
  );
};

export default LandingPage;
