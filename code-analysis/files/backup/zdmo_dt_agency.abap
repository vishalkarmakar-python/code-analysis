@EndUserText.label : 'Draft Table for Agency'
@AbapCatalog.enhancement.category : #EXTENSIBLE_ANY
@AbapCatalog.tableCategory : #TRANSPARENT
@AbapCatalog.deliveryClass : #A
@AbapCatalog.dataMaintenance : #RESTRICTED
define table zdmo_dt_agency {
  key mandt          : mandt not null;
  key agencyid       : /dmo/agency_id not null;
  key draftuuid      : sdraft_uuid not null;
  name               : /dmo/agency_name;
  phonenumber        : /dmo/phone_number;
  emailaddress       : /dmo/email_address;
  webaddress         : /dmo/web_address;
  street             : /dmo/street;
  city               : /dmo/city;
  postalcode         : /dmo/postal_code;
  country            : landx;
  countrycode        : land1;
  localcreatedby     : abp_creation_user;
  localcreatedat     : abp_creation_tstmpl;
  locallastchangedby : abp_locinst_lastchange_user;
  locallastchangedat : abp_locinst_lastchange_tstmpl;
  lastchangedat      : abp_lastchange_tstmpl;
  "%admin"           : include sych_bdl_draft_admin_inc;

}