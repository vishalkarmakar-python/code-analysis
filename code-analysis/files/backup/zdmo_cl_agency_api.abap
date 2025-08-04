class zdmo_cl_agency_api definition
  inheriting from cl_abap_behv
  create public
  public final.

  public section.
    types:
      tt_agency_create  type table    for          create zdmo_r_agency\\Agency,
      tt_agency_update  type table    for          update zdmo_r_agency\\Agency,
      tt_agency_delete  type table    for          delete zdmo_r_agency\\Agency,
      tt_agency_read    type table    for read     import zdmo_r_agency\\Agency,
      tt_agency_result  type table    for read     result zdmo_r_agency\\Agency,
      tt_mapped_early   type response for mapped   early  zdmo_r_agency,
      tt_mapped_late    type response for mapped   late   zdmo_r_agency,
      tt_failed_early   type response for failed   early  zdmo_r_agency,
      tt_failed_late    type response for failed   late   zdmo_r_agency,
      tt_reported_early type response for reported early  zdmo_r_agency,
      tt_reported_late  type response for reported late   zdmo_r_agency.

    class-methods:
      get_instance
        returning value(ro_instance) type ref to zdmo_cl_agency_api.
    methods:
      create_agency
        importing
          entities type tt_agency_create
        changing
          mapped   type tt_mapped_early
          failed   type tt_failed_early
          reported type tt_reported_early,
      update_agency
        importing
          entities type tt_agency_update
          agency   type tt_agency_result
        changing
          mapped   type tt_mapped_early
          failed   type tt_failed_early
          reported type tt_reported_early,
      delete_agency
        importing
          keys     type tt_agency_delete
        changing
          mapped   type tt_mapped_early
          failed   type tt_failed_early
          reported type tt_reported_early,
      read_agency
        importing
          agency   type tt_agency_read
        changing
          result   type tt_agency_result
          failed   type tt_failed_early
          reported type tt_reported_early,
      adjust_numbers
        changing
          mapped   type tt_mapped_late
          reported type tt_reported_late,
      save_agency,
      destroy_instance.

  private section.
    class-data: gs_agency        type          /dmo/agency,
                gt_agency_create type table of /dmo/agency,
                gt_agency_update type table of /dmo/agency,
                gt_agency_delete type table of /dmo/agency,
                late_agency_id   type /dmo/agency_id value '900001'.

endclass.

class zdmo_cl_agency_api implementation.
  method get_instance.
    ro_instance = cond #( when ro_instance is bound then ro_instance else new #( ) ).
  endmethod.

  method create_agency.
    check entities is not initial.
    loop at entities assigning field-symbol(<lfs_entities>).
      gs_agency                  = corresponding #( <lfs_entities> mapping from entity ).
      "Assigning Temporary Agency ID.
      gs_agency-agency_id        = cond #( when <lfs_entities>-AgencyId is not initial
                                              then <lfs_entities>-AgencyId
                                              else late_agency_id ).
      get time stamp field gs_agency-last_changed_at.
      append value #( %cid      = <lfs_entities>-%cid
                      AgencyId  = gs_agency-agency_id ) to mapped-agency.
      append value #( %cid      = <lfs_entities>-%cid
                      AgencyId  = gs_agency-agency_id
                      %msg      = new_message( id       = '00'
                                               number   = '001'
                                               severity = if_abap_behv_message=>severity-success
                                               v1       = |Travel ID: { gs_agency-agency_id alpha = out }|
                                               v2       = | has been assigned for creation successfully.| )
                      %create   = if_abap_behv=>mk-on ) to reported-agency.
      append gs_agency to gt_agency_create.
      if <lfs_entities>-AgencyId is initial.
        late_agency_id = late_agency_id + 1.
      endif.
      clear: gs_agency.
    endloop.
  endmethod.

  method update_agency.
    check entities is not initial and agency is not initial.
    loop at entities assigning field-symbol(<lfs_entities>).
      gt_agency_update = value #( base gt_agency_update
                                    for <lfs_agency> in agency
                                      from line_index( agency[ AgencyId = <lfs_entities>-AgencyId ] )
                                      where ( AgencyId = <lfs_entities>-AgencyId ) ( agency_id            = cond #( when <lfs_entities>-%control-AgencyId eq if_abap_behv=>mk-on
                                                                                                                      then <lfs_entities>-AgencyId
                                                                                                                      else <lfs_agency>-AgencyId )
                                                                                     name                 = cond #( when <lfs_entities>-%control-Name eq if_abap_behv=>mk-on
                                                                                                                      then <lfs_entities>-Name
                                                                                                                      else <lfs_agency>-Name )
                                                                                     phone_number         = cond #( when <lfs_entities>-%control-PhoneNumber eq if_abap_behv=>mk-on
                                                                                                                      then <lfs_entities>-PhoneNumber
                                                                                                                      else <lfs_agency>-PhoneNumber )
                                                                                     email_address        = cond #( when <lfs_entities>-%control-EmailAddress eq if_abap_behv=>mk-on
                                                                                                                      then <lfs_entities>-EmailAddress
                                                                                                                      else <lfs_agency>-EmailAddress )
                                                                                     web_address          = cond #( when <lfs_entities>-%control-WebAddress eq if_abap_behv=>mk-on
                                                                                                                      then <lfs_entities>-WebAddress
                                                                                                                      else <lfs_agency>-WebAddress )
                                                                                     street                = cond #( when <lfs_entities>-%control-Street eq if_abap_behv=>mk-on
                                                                                                                       then <lfs_entities>-Street
                                                                                                                       else <lfs_agency>-street )
                                                                                     city                  = cond #( when <lfs_entities>-%control-City eq if_abap_behv=>mk-on
                                                                                                                       then <lfs_entities>-City
                                                                                                                       else <lfs_agency>-city )
                                                                                     postal_code           = cond #( when <lfs_entities>-%control-PostalCode eq if_abap_behv=>mk-on
                                                                                                                       then <lfs_entities>-PostalCode
                                                                                                                       else <lfs_agency>-PostalCode )
                                                                                     country_code          = cond #( when <lfs_entities>-%control-CountryCode eq if_abap_behv=>mk-on
                                                                                                                       then <lfs_entities>-CountryCode
                                                                                                                       else <lfs_agency>-CountryCode )
                                                                                     local_created_by      = cond #( when <lfs_entities>-%control-LocalCreatedBy eq if_abap_behv=>mk-on
                                                                                                                       then <lfs_entities>-LocalCreatedBy
                                                                                                                       else <lfs_agency>-LocalCreatedBy )
                                                                                     local_created_at      = cond #( when <lfs_entities>-%control-LocalCreatedAt eq if_abap_behv=>mk-on
                                                                                                                       then <lfs_entities>-LocalCreatedAt
                                                                                                                       else <lfs_agency>-LocalCreatedAt )
                                                                                     local_last_changed_by = cond #( when <lfs_entities>-%control-LocalLastChangedBy eq if_abap_behv=>mk-on
                                                                                                                       then <lfs_entities>-LocalLastChangedBy
                                                                                                                       else |{ sy-uname }| )
                                                                                     local_last_changed_at = cond #( when <lfs_entities>-%control-LocalLastChangedAt eq if_abap_behv=>mk-on
                                                                                                                       then <lfs_entities>-LocalLastChangedAt
                                                                                                                       else |{ sy-datum }{ sy-uzeit }| )
                                                                                     last_changed_at       = cond #( when <lfs_entities>-%control-LastChangedAt eq if_abap_behv=>mk-on
                                                                                                                       then <lfs_entities>-LastChangedAt
                                                                                                                       else |{ sy-datum }{ sy-uzeit }| ) ) ).
      reported-agency = value #( base reported-agency
                                 for <lfs_agency> in agency
                                  from line_index( agency[ AgencyId = <lfs_entities>-AgencyId ] )
                                  where ( AgencyId = <lfs_entities>-AgencyId ) ( %cid      = <lfs_entities>-%cid_ref
                                                                                 %pid      = <lfs_entities>-%pid
                                                                                 AgencyId  = <lfs_entities>-AgencyId
                                                                                 %msg      = new_message( id       = '00'
                                                                                                          number   = '001'
                                                                                                          severity = if_abap_behv_message=>severity-success
                                                                                                          v1       = |Agency ID: { <lfs_entities>-AgencyId alpha = out }|
                                                                                                          v2       = | has been assigned for updation successfully| )
                                                                                 %update   = if_abap_behv=>mk-on ) ).
    endloop.
  endmethod.

  method delete_agency.
    check keys is not initial.
    gt_agency_delete = corresponding #( keys mapping from entity ).
    mapped-agency    = corresponding #( keys ).
    reported-agency = value #( base reported-agency
                               for <lfs_keys> in keys ( %cid = <lfs_keys>-%cid_ref
                                                        %pid      = <lfs_keys>-%pid
                                                        AgencyId  = <lfs_keys>-AgencyId
                                                        %msg      = new_message( id       = '00'
                                                                                 number   = '001'
                                                                                 severity = if_abap_behv_message=>severity-success
                                                                                 v1       = |Agency ID: { <lfs_keys>-AgencyId alpha = out }|
                                                                                 v2       = | has been assigned for deletion successfully| )
                                                        %delete   = if_abap_behv=>mk-on ) ).
  endmethod.

  method read_agency.
    check agency is not initial.
    select
      from /dmo/agency as db
      join @agency as ag
      on db~agency_id = ag~AgencyId
    fields
      db~*
    into table @data(lt_agency).
    if sy-subrc is initial.
      loop at agency assigning field-symbol(<lfs_agency>).
        try.
            data(ls_agency) = value #( lt_agency[ agency_id = <lfs_agency>-AgencyId ] ).
            result = value #( base result
                                for <ls_agency> in lt_agency where ( agency_id = <lfs_agency>-AgencyId ) ( corresponding #( <ls_agency> mapping to entity ) ) ).
          catch cx_sy_itab_line_not_found into data(ls_catch).
            failed-agency = value #( base failed-agency ( %pid        = <lfs_agency>-%pid
                                                          %fail-cause = if_abap_behv=>cause-not_found
                                                          AgencyId    = <lfs_agency>-AgencyId ) ).
            reported-agency = value #( base reported-agency ( AgencyId = <lfs_agency>-AgencyId
                                                              %msg     = new_message( id       = '00'
                                                                                      number   = '001'
                                                                                      severity = if_abap_behv_message=>severity-error
                                                                                      v1       = |Agency ID: { <lfs_agency>-AgencyId }|
                                                                                      v2       = | do not exists.| ) ) ).
        endtry.
      endloop.
    endif.
  endmethod.

  method adjust_numbers.
    "For Create.
    if gt_agency_create is not initial.
      try.
          cl_numberrange_runtime=>number_get(
            exporting
              nr_range_nr       = '01'
              object            = '/DMO/AGNCY'
              quantity          = conv #( lines( gt_agency_create ) )
            importing
              number            = data(lv_agency_id)
              returncode        = data(lv_return_code)
              returned_quantity = data(lv_returned_quantity)
          ).
          loop at gt_agency_create assigning field-symbol(<lfs_create>).
            append value #( %tmp     = value #( agencyid = <lfs_create>-agency_id )
                            agencyid = lv_agency_id ) to mapped-agency.
            append value #( agencyid = lv_agency_id
                            %create  = if_abap_behv=>mk-on
                            %msg     = new_message( id       = '00'
                                                    number   = '001'
                                                    severity = if_abap_behv_message=>severity-success
                                                    v1       = |Agency ID: { lv_agency_id alpha = out }|
                                                    v2       = | created successfully.| ) ) to reported-agency.
            <lfs_create>-agency_id   = lv_agency_id.
            lv_agency_id = lv_agency_id + 1.
          endloop.
        catch cx_number_ranges into data(lx_number_ranges).
          append value #( %msg = lx_number_ranges ) to reported-agency.
      endtry.
      "For Update.
    elseif gt_agency_update is not initial.
      loop at gt_agency_update assigning field-symbol(<lfs_update>)..
        append value #( agencyid = <lfs_update>-agency_id ) to mapped-agency.
        append value #( agencyid = <lfs_update>-agency_id
                        %update  = if_abap_behv=>mk-on
                        %msg     = new_message( id       = '00'
                                                number   = '001'
                                                severity = if_abap_behv_message=>severity-success
                                                v1       = |Agency ID: { <lfs_update>-agency_id alpha = out }|
                                                v2       = | updated successfully.| ) ) to reported-agency.
      endloop.
      "For Delete.
    elseif gt_agency_delete is not initial.
      loop at gt_agency_delete assigning field-symbol(<lfs_delete>).
        append value #( agencyid = <lfs_delete>-agency_id
                        %delete  = if_abap_behv=>mk-on
                        %msg     = new_message( id       = '00'
                                                number   = '001'
                                                severity = if_abap_behv_message=>severity-success
                                                v1       = |Agency ID: { <lfs_delete>-agency_id alpha = out }|
                                                v2       = | deleted successfully.| ) ) to reported-agency.
      endloop.
    endif.
  endmethod.

  method save_agency.
    insert /dmo/agency from table @gt_agency_create.
    modify /dmo/agency from table @gt_agency_update.
    delete /dmo/agency from table @gt_agency_delete.
  endmethod.

  method destroy_instance.
    clear: me->gt_agency_create,
           me->gt_agency_update,
           me->gt_agency_delete.
  endmethod.

endclass.