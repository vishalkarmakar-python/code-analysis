unmanaged implementation in class zdmo_cl_agency unique;
strict ( 2 );

define behavior for zdmo_r_agency alias Agency
late numbering
lock master
authorization master ( instance )
etag master LastChangedAt
{
  create;
  update;
  delete;
  field ( mandatory ) Name, PhoneNumber, EmailAddress, WebAddress;
  mapping for /dmo/agency
  {
    AgencyId = agency_id;
    Name = name;
    PhoneNumber = phone_number;
    EmailAddress = email_address;
    WebAddress = web_address;
    Street = street;
    City = city;
    PostalCode = postal_code;
    CountryCode = country_code;
    LocalCreatedBy = local_created_by;
    LocalCreatedAt = local_created_at;
    LocalLastChangedBy = local_last_changed_by;
    LocalLastChangedAt = local_last_changed_at;
    LastChangedAt = last_changed_at;
  }
}