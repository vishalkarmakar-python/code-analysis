@AccessControl.authorizationCheck: #NOT_REQUIRED
@EndUserText.label: 'Root Entity for Agency'
define root view entity zdmo_r_agency
  as select from /dmo/agency as ag
    inner join   t005t       as co on ag.country_code = co.land1
{
  key ag.agency_id             as AgencyId,
      ag.name                  as Name,
      ag.phone_number          as PhoneNumber,
      ag.email_address         as EmailAddress,
      ag.web_address           as WebAddress,
      ag.street                as Street,
      ag.city                  as City,
      ag.postal_code           as PostalCode,
      co.landx                 as Country,
      ag.country_code          as CountryCode,
      @Semantics.user.createdBy: true
      ag.local_created_by      as LocalCreatedBy,
      @Semantics.systemDateTime.createdAt: true
      ag.local_created_at      as LocalCreatedAt,
      @Semantics.user.localInstanceLastChangedBy: true
      ag.local_last_changed_by as LocalLastChangedBy,
      @Semantics.systemDateTime.localInstanceLastChangedAt: true
      ag.local_last_changed_at as LocalLastChangedAt,
      @Semantics.systemDateTime.lastChangedAt: true
      ag.last_changed_at       as LastChangedAt
}
where
  co.spras = $session.system_language
