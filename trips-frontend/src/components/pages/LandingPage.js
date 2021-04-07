import React from "react";
import tw from "twin.macro"; //eslint-disable-line
import dayjs from "dayjs";

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
  const [bestTours] = useFetchApi({ url: "/tours/tours/" }, []);
  const [incomingTrips] = useFetchApi(
    {
      url: "/tours/instances/",
      params: { departure_time_after: dayjs().format("YYYY-MM-DD") },
    },
    []
  );

  const adaptTrips = (trips) => {
    const cards = [];
    trips.forEach((trip) => {
      cards.push({
        imageSrc: trip.tour.main_image,
        headerText: trip.tour.destination,
        price: trip.price,
        title: trip.tour.short_description,
        fromDate: dayjs(trip.departure_time).format("DD MMM YY"),
        toDate: dayjs(trip.return_time).format("DD MMM YY"),
        locationText: trip.tour.country,
      });
    });
    return cards;
  };

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
        cards={adaptTrips(incomingTrips.data)}
      />
      <TwoColSingleFeatureWithStats />
      <TwoColumnWithImageAndProfilePictureReview textOnLeft={true} />
      <FaqWithSideImage />
    </>
  );
};

export default LandingPage;
