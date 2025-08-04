class lhc_Agency definition
  inheriting from cl_abap_behavior_handler.
  private section.
    methods:
      get_instance_authorizations for instance authorization
        importing keys request requested_authorizations for Agency result result,
      create for modify
        importing entities for create Agency,
      update for modify
        importing entities for update Agency,
      delete for modify
        importing keys for delete Agency,
      read for read
        importing keys for read Agency result result,
      lock for lock
        importing keys for lock Agency.

endclass.

class lhc_Agency implementation.

  method get_instance_authorizations.
  endmethod.

  method create.
    zdmo_cl_agency_api=>get_instance(  )->create_agency(
      exporting
        entities = entities
      changing
        mapped   = mapped
        failed   = failed
        reported = reported
    ).
  endmethod.

  method update.
    read entities of zdmo_r_agency in local mode
      entity Agency
      all fields with corresponding #( entities )
    result data(lt_agency)
    failed data(lt_failed)
    reported data(lt_reported).
    zdmo_cl_agency_api=>get_instance(  )->update_agency(
      exporting
        entities = entities
        agency   = lt_agency
      changing
        mapped   = mapped
        failed   = failed
        reported = reported
    ).
  endmethod.

  method delete.
    zdmo_cl_agency_api=>get_instance(  )->delete_agency(
      exporting
        keys     = keys
      changing
        mapped   = mapped
        failed   = failed
        reported = reported
    ).
  endmethod.

  method read.
    zdmo_cl_agency_api=>get_instance(  )->read_agency(
      exporting
        agency   = keys
      changing
        result   = result
        failed   = failed
        reported = reported
    ).
  endmethod.

  method lock.
  endmethod.

endclass.

class lsc_zdmo_r_agency definition inheriting from cl_abap_behavior_saver.
  protected section.

    methods:
      finalize redefinition,
      check_before_save redefinition,
      adjust_numbers redefinition,
      save redefinition,
      cleanup redefinition,
      cleanup_finalize redefinition.

endclass.

class lsc_zdmo_r_agency implementation.

  method finalize.
  endmethod.

  method check_before_save.
  endmethod.

  method adjust_numbers.
    zdmo_cl_agency_api=>get_instance(  )->adjust_numbers(
      changing
        mapped   = mapped
        reported = reported
    ).
  endmethod.

  method save.
    zdmo_cl_agency_api=>get_instance( )->save_agency( ).
  endmethod.

  method cleanup.
    zdmo_cl_agency_api=>get_instance( )->destroy_instance( ).
  endmethod.

  method cleanup_finalize.
  endmethod.

endclass.