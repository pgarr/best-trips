import React from "react";
import tw, { styled } from "twin.macro";
import { css } from "styled-components/macro"; //eslint-disable-line
import { PrimaryButton as PrimaryButtonBase } from "components/misc/Buttons.js";
import { ReactComponent as LocationIcon } from "feather-icons/dist/icons/map-pin.svg";
import { ReactComponent as TimeIcon } from "feather-icons/dist/icons/clock.svg";
import { ReactComponent as TrendingIcon } from "feather-icons/dist/icons/trending-up.svg";

const Card = tw.div`mx-auto xl:mx-0 xl:ml-auto max-w-sm md:max-w-xs lg:max-w-sm xl:max-w-xs`;
const CardImage = styled.div((props) => [
  `background-image: url("${props.imageSrc}");`,
  tw`h-80 bg-cover bg-center rounded`,
]);

const CardText = tw.div`mt-4`;
const CardHeader = tw.div`flex justify-between items-center`;
const CardHeaderText = tw.div`text-primary-500 font-bold text-lg`;
const CardPrice = tw.div`font-semibold text-sm text-gray-600`;
const CardPriceAmount = tw.span`font-bold text-gray-800 text-lg`;
const CardTitle = tw.h5`text-xl mt-4 font-bold`;
const CardMeta = styled.div`
  ${tw`flex flex-row flex-wrap justify-between sm:items-center font-semibold tracking-wide text-gray-600 uppercase text-xs`}
`;
const CardMetaFeature = styled.div`
  ${tw`flex items-center mt-4`}
  svg {
    ${tw`w-5 h-5 mr-1`}
  }
`;
const CardAction = tw(PrimaryButtonBase)`w-full mt-8`;

const TourInstanceCard = ({ card }) => {
  return (
    <Card>
      <CardImage imageSrc={card.imageSrc} />
      <CardText>
        <CardHeader>
          <CardHeaderText>{card.headerText}</CardHeaderText>
          <CardPrice>
            <CardPriceAmount>{card.price}</CardPriceAmount>
          </CardPrice>
        </CardHeader>
        <CardTitle>{card.title}</CardTitle>
        <CardMeta>
          <CardMetaFeature>
            <TimeIcon /> {card.fromDate} - {card.toDate}
          </CardMetaFeature>
          <CardMetaFeature>
            <LocationIcon /> {card.locationText}
          </CardMetaFeature>
        </CardMeta>
        <CardAction>Book Now</CardAction>
      </CardText>
    </Card>
  );
};

export default TourInstanceCard;
