@Metadata.layer: #CUSTOMER
@UI.headerInfo:
{
  typeName: 'Agency',
  typeNamePlural: 'Agencys',
  title.type: #STANDARD,
  title.value: 'AgencyId',
  description.type: #STANDARD,
  description.value: 'Name'
}
@UI.presentationVariant:
[{
    sortOrder: [{ by: 'AgencyId', direction: #ASC }],
    maxItems: 100
}]
annotate entity zdmo_p_agency with
{
  @UI.facet:
  [
    {
      id: 'id_Agency',
      type: #FIELDGROUP_REFERENCE,
      purpose: #STANDARD,
      targetQualifier: 'tqAgency',
      position: 10,
      label: 'Agency Details'
    },
    {
      id: 'id_Contact',
      type: #FIELDGROUP_REFERENCE,
      purpose: #STANDARD,
      targetQualifier: 'tqContact',
      position: 20,
      label: 'Agency Contact'
    },
    {
      id: 'id_Address',
      type: #FIELDGROUP_REFERENCE,
      purpose: #STANDARD,
      targetQualifier: 'tqAddress',
      position: 30,
      label: 'Agency Address'
    }
  ]
  @Consumption.valueHelpDefinition:
  [{
    entity:{ name: 'zdmo_vh_agency', element: 'AgencyId' },
    additionalBinding: [{ element: 'CountryCode', localElement: 'CountryCode' }]
  }]
  @UI.selectionField: [{ position: 20 }]
  @UI.lineItem:[{ position: 10, label: 'Agency ID' }]
  AgencyId;
  @UI.fieldGroup: [{ qualifier: 'tqAgency', position: 11, label: 'Agency Name' }]
  Name;
  @UI.lineItem:[{ position: 20, label: 'Phone' }]
  @UI.fieldGroup: [{ qualifier: 'tqContact', position: 21, label: 'Phone Number' }]
  PhoneNumber;
  @UI.lineItem:[{ position: 30, label: 'Email' }]
  @UI.fieldGroup: [{ qualifier: 'tqContact', position: 22, label: 'Email' }]
  EmailAddress;
  @UI.fieldGroup: [{ qualifier: 'tqContact', position: 23, label: 'Website' }]
  WebAddress;
  @UI.fieldGroup: [{ qualifier: 'tqAddress', position: 31, label: 'Street' }]
  Street;
  @UI.lineItem:[{ position: 40, label: 'City' }]
  @UI.fieldGroup: [{ qualifier: 'tqAddress', position: 32, label: 'City' }]
  City;
  @UI.fieldGroup: [{ qualifier: 'tqAddress', position: 33, label: 'Pin Code' }]
  PostalCode;
  @UI.lineItem:[{ position: 50, label: 'Country' }]
  Country;
  @Consumption.valueHelpDefinition:
  [{
    entity:{ name: 'za4h_vh_country', element: 'CountryCode' }
  }]
  @UI.selectionField: [{ position: 10 }]
  @UI.fieldGroup: [{ qualifier: 'tqAddress', position: 34, label: 'Country' }]
  CountryCode;
}