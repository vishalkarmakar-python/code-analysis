@AbapCatalog.viewEnhancementCategory: [#NONE]
@Search.searchable: true
@Metadata.ignorePropagatedAnnotations: true
@ObjectModel.dataCategory: #VALUE_HELP
@ObjectModel.usageType.serviceQuality: #X
@ObjectModel.usageType.sizeCategory: #S
@ObjectModel.usageType.dataClass: #MIXED
@AccessControl.authorizationCheck: #NOT_REQUIRED
@EndUserText.label: 'Value Help for Agency'
define view entity zdmo_vh_agency
  as select from zdmo_r_agency
{
      @Search.defaultSearchElement: true
      @Search.fuzzinessThreshold: 0.8
  key AgencyId,
      @Search.defaultSearchElement: true
      @Search.fuzzinessThreshold: 0.8
      Name,
      PhoneNumber,
      Street,
      City,
      PostalCode,
      Country,
      @UI.hidden: true
      CountryCode
}
