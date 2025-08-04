@ObjectModel.semanticKey: [ 'AgencyId' ]
@Search.searchable: true
@Metadata.allowExtensions: true
@AccessControl.authorizationCheck: #NOT_REQUIRED
@EndUserText.label: 'Projection Entity for Agency'
define root view entity zdmo_p_agency
  provider contract transactional_query
  as projection on zdmo_r_agency
{
      @ObjectModel.text.element: [ 'Name' ]
      @Search.defaultSearchElement: true
      @Search.fuzzinessThreshold: 0.8
  key AgencyId,
      @Semantics.text: true
      @Search.defaultSearchElement: true
      @Search.fuzzinessThreshold: 0.8
      Name,
      PhoneNumber,
      EmailAddress,
      WebAddress,
      Street,
      City,
      PostalCode,
      Country,
      CountryCode,
      @Semantics.user.createdBy: true
      LocalCreatedBy,
      @Semantics.systemDateTime.createdAt: true
      LocalCreatedAt,
      @Semantics.user.localInstanceLastChangedBy: true
      LocalLastChangedBy,
      @Semantics.systemDateTime.localInstanceLastChangedAt: true
      LocalLastChangedAt,
      @Semantics.systemDateTime.lastChangedAt: true
      LastChangedAt
}
