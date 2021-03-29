import React from "react";
import tw from "twin.macro"; //eslint-disable-line

import Hero from "components/blocks/HeroWithImage";
import ThreeColSlider from "components/blocks/ThreeColSlider";
import TwoPreviewsWithDescription from "components/blocks/TwoPreviewsWithDescription";
import TwoColSingleFeatureWithStats from "components/blocks/StatsWithImage";
import TwoColumnWithImageAndProfilePictureReview from "components/blocks/ReviewsWithImage";
import FaqWithSideImage from "components/blocks/FaqWithSideImage";
import useFetchApi from "helpers/customHooks/useFetchApi";

const heroHeading = (
  <>
    Amazing places
    <wbr />
    <br />
    <span tw="text-primary-500">Long lasting memories</span>
  </>
);
const heroDescription =
  "We have been organizing tours around the world for 5 years. We guarantee unforgettable moments in the most wonderful corners of the globe.";
const heroPrimaryActionText = "Sign Up";
const heroSecondaryActionText = "Search Tours";

const LandingPage = () => {
  const [{ data, isLoading }, doFetch] = useFetchApi(
    { url: "/tours/tours/" },
    []
  );

  const cards = [
    {
      imageSrc:
        "https://images.unsplash.com/photo-1553194587-b010d08c6c56?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=768&q=80",
      headerText: "Poznań",
      price: "$99",
      title: "A Trip to the Bahamas and the Carribean Ocean",
      fromDate: "10 May",
      toDate: "24 May",
      locationText: "Poland",
    },
    {
      imageSrc:
        "https://images.unsplash.com/photo-1584200186925-87fa8f93be9b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=768&q=80",
      headerText: "Sydney",
      price: "$1690",
      title: "Cruise to the Mariana Trench and the Phillipines",
      fromDate: "10 May",
      toDate: "24 May",
      locationText: "Australia",
    },
  ];

  return (
    <>
      <Hero
        heading={heroHeading}
        description={heroDescription}
        primaryActionUrl="/register"
        primaryActionText={heroPrimaryActionText}
        secondaryActionUrl="/tours"
        secondaryActionText={heroSecondaryActionText}
      />
      <ThreeColSlider />
      <TwoPreviewsWithDescription
        title="Incoming tours"
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua enim
                ad minim veniam."
        primaryLinkDesc="View all tours"
        cards={cards}
      />
      <TwoColSingleFeatureWithStats />
      <TwoColumnWithImageAndProfilePictureReview textOnLeft={true} />
      <FaqWithSideImage />
    </>
  );
};

export default LandingPage;
