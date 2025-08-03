from typing import Dict, List


class ABAP:
    """
    Enhanced class to hold separators used in the document generator.
    This class provides comprehensive text splitters for all ABAP code types including:
    - Classical ABAP reports, function modules, BAPIs
    - RAP objects (CDS entities, behavior definitions)
    - Enhancement framework (BADIs, User Exits, Customer Exits)
    - Modern ABAP syntax (7.4+, EML)
    - Cloud-specific constructs
    """

    # New: Compound keywords for separated word patterns
    DOCUMENT_KEYWORDS: Dict[str, List[str]] = {
        # === Database Objects ===
        "DATABASE TABLE": [
            "tableCategory",
            "deliveryClass",
            "dataMaintenance",
            "define",
            "table",
            "key",
            "include",
        ],
        "STRUCTURE": [
            "define",
            "structure",
            "key",
            "include",
        ],
        # === ABAP RESTful Application Programming Model ===
        "PROJECTION ENTITY": [
            "define",
            "root",
            "view",
            "entity",
            "provider",
            "contract",
            "transactional_query",
            "projection",
        ],
        "ROOT ENTITY": [
            "define",
            "root",
            "view",
            "entity",
            "select",
            "from",
            "join",
        ],
        "ENTITY": [
            "define",
            "view",
            "entity",
            "select",
            "from",
            "join",
        ],
        "VALUE HELP ENTITY": [
            "objectmodel",
            "datacategory",
            "#value_help",
            "servicequality",
            "define",
            "view",
            "entity",
            "select",
            "from",
            "join",
        ],
        "METADATA ENTITY": [
            "metadata",
            "layer",
            "annotate",
            "withentity",
        ],
        "ABSTRACT ENTITY": [
            "define",
            "abstract",
            "entity",
        ],
        "CUSTOM ENTITY": [
            "define",
            "custom",
            "entity",
        ],
        "SERVICE DEFINITION": [
            "define",
            "service",
            "expose",
        ],
        "BEHAVIOR PROJECTION": [
            "projection",
            "strict",
            "define",
            "behavior",
            "use",
            "create",
            "update",
            "delete",
            "action",
            "determination",
            "validation",
        ],
        "UNMANAGED BEHAVIOR DEFINITION": [
            "unmanaged",
            "implementation",
            "class",
            "define",
            "behavior",
            "for",
        ],
        "MANAGED BEHAVIOR DEFINITION": [
            "managed",
            "implementation",
            "class",
            "define",
            "behavior",
            "for",
        ],
        # === Object-Oriented Programming ===
        "CLASS": [
            "class",
            "definition",
            "create",
            "interfaces",
            "public",
            "protected",
            "private",
            "final",
            "section",
            "class-methods",
            "methods",
            "implementation",
        ],
        # === Function Modules ===
        "FUNCTION MODULE": [
            "function",
            "importing",
            "exporting",
            "changing",
            "tables",
            "exceptions",
            "value",
            "optional",
            "endfunction",
        ],
        # === Exits ===
        "EXITS": [
            "call",
            "user_exit",
            "customer",
            "function",
            "importing",
            "exporting",
            "changing",
            "tables",
            "exceptions",
            "value",
            "optional",
            "endfunction",
        ],
    }

    SEPARATOR: List[str] = [
        # === RAP Objects & CDS Definitions ===
        "\nDEFINE ROOT VIEW ENTITY",
        "\nDEFINE VIEW ENTITY",
        "\nDEFINE ABSTRACT ENTITY",
        "\nDEFINE CUSTOM ENTITY",
        "\nDEFINE VIEW",
        "\nDEFINE TABLE FUNCTION",
        "\nANNOTATE ENTITY",
        "\nDEFINE ACCESS CONTROL",
        "\nDEFINE SERVICE",
        "\nUNMANAGED IMPLEMENTATION IN CLASS",
        "\nMANAGED IMPLEMENTATION IN CLASS",
        "\nDEFINE BEHAVIOR FOR",
        # === Class, Method & Interface Definitions ===
        "\nCLASS ",
        "\nENDCLASS.",
        "\nMETHOD ",
        "\nENDMETHOD.",
        "\nPUBLIC SECTION.",
        "\nPROTECTED SECTION.",
        "\nPRIVATE SECTION.",
        "\nINTERFACE ",
        "\nENDINTERFACE.",
    ]

    @classmethod
    def get_document_keywords(cls) -> Dict[str, List[str]]:
        """
        Returns the enhanced keyword dictionary with all ABAP constructs.
        """
        return cls.DOCUMENT_KEYWORDS.copy()

    @classmethod
    def get_separators(cls) -> List[str]:
        """
        Returns the enhanced separator list with all ABAP constructs.
        """
        return cls.SEPARATOR.copy()

    @classmethod
    def calculate_chunk_size(cls, content: str, chunk_size: int) -> int:
        # Adaptive chunk sizes based on document type
        pre_defined_chunk_size: Dict[str, int] = {
            "PROJECTION ENTITY": int(chunk_size * 1.1),
            "ROOT ENTITY": int(chunk_size * 1.1),
            "VALUE HELP ENTITY": int(chunk_size * 1.1),
            "METADATA ENTITY": int(chunk_size * 2.5),
            "ABSTRACT ENTITY": int(chunk_size * 1.1),
            "CUSTOM ENTITY": int(chunk_size * 1.5),
            "SERVICE DEFINITION": int(chunk_size * 0.5),
            "BEHAVIOR PROJECTION": int(chunk_size * 1.0),
            "UNMANAGED BEHAVIOR DEFINITION": int(chunk_size * 2.0),
            "MANAGED BEHAVIOR DEFINITION": int(chunk_size * 1.5),
            "CLASS": int(chunk_size * 1.5),
            "FUNCTION_MODULE": int(chunk_size * 0.9),
            "EXITS": int(chunk_size * 0.5),
            "ENHANCEMENT": int(chunk_size * 0.8),
            "INCLUDE_PROGRAM": int(chunk_size * 0.7),
            "CLASSICAL_REPORT": chunk_size,
            "DIALOG_PROGRAM": chunk_size,
            "GENERIC_ABAP": chunk_size,
        }

        return pre_defined_chunk_size.get(content, chunk_size)
