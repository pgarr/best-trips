import React from "react";
import tw, { styled } from "twin.macro";
import { PrimaryButton as PrimaryButtonBase } from "components/misc/Buttons";
import { ReactComponent as CallendarIcon } from "feather-icons/dist/icons/calendar.svg";
import { ReactComponent as LocationIcon } from "feather-icons/dist/icons/map-pin.svg";
import { ReactComponent as StarIcon } from "feather-icons/dist/icons/star.svg";

const Card = tw.div`h-full flex! flex-col sm:border max-w-sm sm:rounded-tl-4xl sm:rounded-br-5xl relative focus:outline-none`;
const CardImage = styled.div((props) => [
  `background-image: url("${props.imageSrc}");`,
  tw`w-full h-56 sm:h-64 bg-cover bg-center rounded sm:rounded-none sm:rounded-tl-4xl`,
]);

const TextInfo = tw.div`py-6 sm:px-10 sm:py-6`;
const TitleReviewContainer = tw.div`flex flex-col sm:flex-row sm:justify-between sm:items-center`;
const Title = tw.h5`text-2xl font-bold`;

const RatingsInfo = styled.div`
  ${tw`flex items-center sm:ml-4 mt-2 sm:mt-0`}
  svg {
    ${tw`w-6 h-6 text-yellow-500 fill-current`}
  }
`;
const Rating = tw.span`ml-2 font-bold`;

const Description = tw.p`text-sm leading-loose mt-2 sm:mt-4`;

const SecondaryInfoContainer = tw.div`flex flex-col sm:flex-row mt-2 sm:mt-4`;
const IconWithText = tw.div`flex items-center mr-6 my-2 sm:my-0`;
const IconContainer = styled.div`
  ${tw`inline-block rounded-full p-2 bg-gray-700 text-gray-100`}
  svg {
    ${tw`w-3 h-3`}
  }
`;
const Text = tw.div`ml-2 text-sm font-semibold text-gray-800`;

const PrimaryButton = tw(
  PrimaryButtonBase
)`mt-auto sm:text-lg rounded-none w-full rounded sm:rounded-none sm:rounded-br-4xl py-3 sm:py-6`;

const TourPreviewCard = ({ card, buttonDescription }) => {
  return (
    <Card>
      <CardImage imageSrc={card.imageSrc} />
      <TextInfo>
        <TitleReviewContainer>
          <Title>{card.destination}</Title>
          <RatingsInfo>
            <StarIcon />
            <Rating>{card.rating}</Rating>
          </RatingsInfo>
        </TitleReviewContainer>
        <SecondaryInfoContainer>
          <IconWithText>
            <IconContainer>
              <LocationIcon />
            </IconContainer>
            <Text>{card.locationText}</Text>
          </IconWithText>
          <IconWithText>
            <IconContainer>
              <CallendarIcon />
            </IconContainer>
            <Text>{card.duration}</Text>
          </IconWithText>
        </SecondaryInfoContainer>
        <Description>{card.description}</Description>
      </TextInfo>
      <PrimaryButton>{buttonDescription}</PrimaryButton>
    </Card>
  );
};

export default TourPreviewCard;
