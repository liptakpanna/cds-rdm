import { BasicCERNInformation } from "../../components/deposit/BasicInformation";
import { CDSCarouselItem } from "../../components/communities_carousel/overrides/CarouselItem";
import { CDSCommunitiesCarousel } from "../../components/communities_carousel/overrides/CommunitiesCarousel";
import { CDSRecordsList } from "../../components/frontpage/overrides/RecordsList";
import { CDSRecordsResultsListItem } from "../../components/frontpage/overrides/RecordsResultsListItem";

export const overriddenComponents = {
  "InvenioAppRdm.RecordsList.layout": CDSRecordsList,
  "InvenioAppRdm.RecordsResultsListItem.layout": CDSRecordsResultsListItem,
  "InvenioCommunities.CommunitiesCarousel.layout": CDSCommunitiesCarousel,
  "InvenioCommunities.CarouselItem.layout": CDSCarouselItem,
  "InvenioAppRdm.Deposit.AccordionFieldBasicInformation.placeholder":
    BasicCERNInformation,
  "InvenioAppRdm.Deposit.CustomFields.container": () => null,
};
