from typing import Dict, List


class ABAP:
    """
    Class to hold the separators used in the document generator.
    This class provides methods to create text splitters for ABAP code and generic documents.
    """

    KEYWORD: Dict[str, str] = {
        # CDS Entities.
        "DEFINE ROOT VIEW ENTITY": "ROOT ENTITY",  # CDS Root Entity
        "PROVIDER CONTRACT TRANSACTIONAL_QUERY": "PROJECTION ENTITY",  # CDS Projection Entity
        "DEFINE VIEW ENTITY": "VIEW ENTITY",  # CDS View Entity
        "DEFINE ABSTRACT ENTITY": "ABSTRACT ENTITY",  # CDS Abstract Entity
        "DEFINE VIEW": "CDS VIEW",  # CDS View
        "DEFINE TABLE FUNCTION": "CDS TABLE FUNCTION",  # CDS Table Function
        "ANNOTATE ENTITY": "METADATA EXTENSION",  # CDS Metadata Extension
        "DEFINE ACCESS CONTROL": "ACCESS CONTROL",  # Start of a DCL (Data Control Language) definition
        "#VALUE_HELP": "VALUE HELP",  # Value Help
        # Global and Local Class Definitions
        "CLASS DEFINITION": "CLASS DEFINITION",  # Class Definition
        "CLASS IMPLEMENTATION": "CLASS IMPLEMENTATION",  # Class Definition
        "METHOD": "METHOD",  # Method Definition
    }

    SEPARATOR: List[str] = [
        # --- RAP (ABAP RESTful Application Programming Model) Object Definitions & Ends ---
        # These are top-level definitions in RAP development.
        "\nDEFINE ROOT VIEW ENTITY",  # Start of a root CDS entity definition (conceptual)
        "\nDEFINE PROJECTION VIEW ENTITY",  # Start of a projection CDS entity definition (conceptual)
        "\nDEFINE VIEW ENTITY",  # Start of a CDS view entity
        "\nDEFINE ABSTRACT ENTITY",  # Start of a CDS abstract entity
        "\nDEFINE CUSTOM ENTITY",  # Start of a CDS custom entity
        "\nDEFINE ENTITY",  # Start of a CDS entity definition
        "\nDEFINE VIEW",  # Start of a CDS view definition
        "\nDEFINE TABLE FUNCTION",  # Start of a CDS table function
        "\nDEFINE HIERARCHY",  # Start of a CDS hierarchy
        "\nDEFINE METADATA EXTENSION",  # Start of a CDS metadata extension
        "\nDEFINE ANNOTATION",  # Start of a CDS annotation definition
        "\nDEFINE ACCESS CONTROL",  # Start of a DCL (Data Control Language) definition
        "\nDEFINE SERVICE DEFINITION",  # Start of a Service Definition
        "\nDEFINE SERVICE BINDING",  # Start of a Service Binding
        # Behavior Definitions (BDEF)
        "\nDEFINE BEHAVIOR FOR",  # Start of a Behavior Definition
        "\nIMPLEMENTATION IN CLASS",  # Part of BDEF, often followed by ABAP class link
        "\nPROJECTION;",  # End of projection behavior definition block
        "\nIMPLEMENTATION;",  # End of implementation block in BDEF
        # While there isn't a universal "END" for all CDS definitions in the same way as ENDCLASS,
        # the start of a new definition or a significant change in structure (like DDL vs. DCL)
        # often implies a boundary. The semicolon ';' often ends CDS statements.
        # --- Major Program/Class/Interface Definitions & Ends ---
        "\nREPORT ",  # Start of a report program
        "\nPROGRAM ",  # Start of a program
        "\nCLASS ",  # Start of a class definition
        "\nENDCLASS.",  # End of a class definition
        "\nINTERFACE ",  # Start of an interface definition
        "\nENDINTERFACE.",  # End of an interface definition
        "\nFUNCTION-POOL.",  # Start of a function group
        # No specific "ENDFUNCTION-POOL." - boundaries are implicit.
        # --- Method/Function/Form/Module Definitions & Ends ---
        "\nMETHOD ",  # Start of a method implementation or definition (in class/interface)
        "\nENDMETHOD.",  # End of a method implementation
        "\nFUNCTION ",  # Start of a function module definition
        "\nENDFUNCTION.",  # End of a function module definition
        "\nFORM ",  # Start of a FORM routine (subroutine)
        "\nENDFORM.",  # End of a FORM routine
        "\nDEFINE ",  # Start of a macro definition
        "\nEND-OF-DEFINITION.",  # End of a macro definition
        # --- Data Definitions and Declarations (often grouped) ---
        # Splitting before these can sometimes isolate data declaration blocks
        "\nTYPES:",  # Start of a structured type definition
        "\nTYPES BEGIN OF",  # Start of a structured type definition
        "\nTYPES END OF",  # End of a structured type definition
        "\nCONSTANTS:",  # Start of a structured constants definition
        "\nCONSTANTS BEGIN OF",  # Start of a structured constants definition
        "\nCONSTANTS END OF",  # End of a structured constants definition
        "\nDATA:",  # Start of a structured data definition
        "\nDATA BEGIN OF",  # Start of a structured data object (less common now, TYPES preferred)
        "\nDATA END OF",  # End of a structured data object
        # --- Control Flow Blocks - Beginnings (if a block itself is very long) ---
        "\nIF ",  # Start of an IF condition
        "\nELSEIF ",  # Start of an ELSEIF condition
        "\nELSE.",  # Start of an ELSE block (often a good split point too)
        "\nENDIF.",  # End of an IF block
        "\nCASE ",  # Start of a CASE statement
        "\nENDCASE.",  # End of a CASE block
        "\nWHEN ",  # Start of a WHEN block within CASE
        "\nLOOP AT",  # Start of a LOOP AT internal table
        "\nENDLOOP.",  # End of a LOOP AT/LOOP AT GROUP block
        "\nWHILE ",  # Start of a WHILE loop
        "\nENDWHILE.",  # End of a WHILE block
        "\nDO ",  # Start of a DO loop
        "\nENDDO.",  # End of a DO block
        "\nTRY.",  # Start of a TRY-CATCH block
        "\nCATCH ",  # Start of a CATCH block
        "\nENDTRY.",  # End of a TRY-CATCH block
        "\nCLEANUP.",  # Start of a CLEANUP block
        "\nSELECT ",  # Start of a SELECT statement (Open SQL)
        "\nSELECT SINGLE",  # Start of a SELECT SINGLE statement (Open SQL)
        "\nENDSELECT.",  # End of a SELECT...ENDSELECT block (obsolete but might exist)
        "\nPROVIDE ",  # Start of a PROVIDE statement (obsolete)
        "\nENDPROVIDE.",  # End of a PROVIDE block (obsolete but might exist)
        # --- Event Blocks (Classical Reports, Dialog Programming) ---
        "\nINITIALIZATION.",  # Initialization event block
        "\nSTART-OF-SELECTION.",  # Start-of-selection event block
        "\nEND-OF-SELECTION.",  # End-of-selection event block
        "\nTOP-OF-PAGE.",  # Top-of-page event block
        "\nEND-OF-PAGE.",  # End-of-page event block
        "\nAT SELECTION-SCREEN",  # At selection-screen event block (various additions)
        "\nAT LINE-SELECTION.",  # At line-selection event block
        "\nAT USER-COMMAND.",  # At user-command event block
        "\nAT PF##.",  # At PF-key event (e.g., AT PF01.) - use cautiously, might be too granular if not careful
        "\nMODULE",  # Start of a PAI/PBO module (Dialog programming)
        "\nENDMODULE",  # End of a PAI/PBO module (Dialog programming)
        # --- Statement Terminators & Formatting ---
        ".\n",  # Period followed by a newline (primary statement terminator)
        ";\n",  # Semicolon followed by a newline (CDS statement terminator)
        ",\n",  # Comma followed by a newline (often separates parameters or list items)
        # --- Full Line Comments (often separate logical sections) ---
        # Standard ABAP comment line
        "\n*",
        # Common separator comment patterns
        "\n*----------------------------------------------------------------------*",
        "\n*&---------------------------------------------------------------------*",
        "\n*=",  # Often used for headings: *= Heading =*
        # Double quote for comments at the beginning of a line (newer style)
        '\n"',
        # --- Blank Lines (visual separation) ---
        "\n\n",  # Two newlines (a blank line)
        # --- Regular Newlines (general fallback if no other structure found) ---
        "\n",  # Single newline
        # --- Less Ideal but Possible Terminators (if line is too long without newline terminator) ---
        ". ",  # Period followed by a space
        "; ",  # Semicolon followed by a space (CDS)
        ", ",  # Comma followed by a space
        # --- Space (as a last resort, will break up tokens) ---
        " ",  # Space character
        # --- Empty string (will split every character - usually not desired, but is the final fallback for the splitter) ---
        "",  # Empty string
    ]
