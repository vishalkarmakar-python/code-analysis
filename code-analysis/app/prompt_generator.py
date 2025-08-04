from langchain_core.documents.base import Document
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import PromptTemplate
from textwrap import dedent
from typing import ClassVar, Self


class PromptGenerator:
    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True

    def create_analysis_prompt(
        self,
        file_name: str,
        document_type: str,
        document: Document,
        document_index: int,
        total_chunks: int,
    ) -> PromptValue:
        """
        Create a prompt for analyzing a document chunk of ABAP code.
        This helps stay within token limits.
        """
        prompt = PromptTemplate(
            input_variables=[
                "file_name",
                "document_type",
                "document_chunk",
            ],
            template=self._analysis_prompt_template,
        )
        return prompt.invoke(
            {
                "file_name": file_name,
                "chunk_type": document_type,
                "chunk_index": document_index,
                "total_chunks": total_chunks,
                "chunk_content": document.page_content,
            }
        )

    @property
    def _analysis_prompt_template(self) -> str:
        """
        Generates a detailed, structured prompt for analyzing a chunk of ABAP code.

        This prompt is specifically tailored for analyzing a wide range of ABAP
        development objects. It instructs the AI to act as a senior ABAP developer,
        identify the object type, and extract technically relevant details into a
        structured, object-specific Markdown format.
        """
        return dedent("""
        You are a senior SAP ABAP developer with over 15 years of experience across the entire ABAP stack, including Core ABAP, ABAP on HANA, Classical ABAP, and modern frameworks like the ABAP RESTful Application Programming Model (RAP).
        Your task is to analyze the provided ABAP code chunk and generate a detailed, structured summary in Markdown format.

        **Context:**
        - File Name: {file_name}
        - Object Type Hint: {chunk_type}
        - Chunk: {chunk_index} of {total_chunks}

        **ABAP Code Chunk:**
        ```abap
        {chunk_content}
        ```

        **Instructions:**
        Analyze the code to identify the precise ABAP object type and provide a structured summary. 
        Your primary goal is to adapt the format of the '1. Object Identification and Purpose' and '2. Technical Analysis' section to accurately and clearly represent the specific type of 
        ABAP object provided. If certain information is not present in this chunk, state that clearly.

        ---

        **1. Object Identification and Purpose:**
        - **Identified Object Type:** (e.g., Global Class, Function Group, Report Program, Behavior Definition, Data Definition/CDS Views or CDS Entities, Database Table)
        - **Purpose:** Briefly describe the main purpose of this object. What business or technical process does it implement?

        ---

        **2. Technical Analysis:**
        - **Database Interaction:** List the database tables/CDS views accessed and the type of operations performed (e.g., SELECT from SFLIGHT, UPDATE on /DMO/TRAVEL, EML call to modify Travel).
        - **Key Components:** Identify the main components or logic blocks (e.g., Methods of a class, Forms in a report, Function Modules in a group, Actions in a BDEF, Selection-screen elements).
        - **Dependencies & Calls:** List any significant external dependencies called from this code (e.g., other classes, function modules, APIs, CDS Views).
        - **Programming Model/Pattern (if applicable):** If a specific design pattern or model is evident (e.g., RAP Managed/Unmanaged, ALV Report, Singleton Class, BAPI), please identify it.

        ---

        Generate a comprehensive yet concise response based *only* on the provided code chunk.
        """)

    def create_single_chunk_analysis_prompt(
        self,
        file_name: str,
        chunk_type: str,
        chunk: Document,
        chunk_index: int,
        total_chunks: int,
    ) -> PromptValue:
        """
        Create a prompt for analyzing a single chunk of ABAP code.
        This helps stay within token limits.
        """
        prompt = PromptTemplate(
            input_variables=[
                "file_name",
                "chunk_type",
                "chunk_index",
                "total_chunks",
                "chunk_content",
            ],
            template=self._abap_prompt_template,
        )

        return prompt.invoke(
            {
                "file_name": file_name,
                "chunk_type": chunk_type,
                "chunk_index": chunk_index,
                "total_chunks": total_chunks,
                "chunk_content": chunk.page_content,
            }
        )

    @property
    def _abap_prompt_template(self) -> str:
        """
        Generates a detailed, structured prompt for analyzing a chunk of ABAP code.

        This prompt is specifically tailored for analyzing a wide range of ABAP
        development objects. It instructs the AI to act as a senior ABAP developer,
        identify the object type, and extract technically relevant details into a
        structured, object-specific Markdown format.
        """
        return dedent("""
        You are a senior SAP ABAP developer with over 15 years of experience across the entire ABAP stack, including Core ABAP, ABAP on HANA, Classical ABAP, and modern frameworks like the ABAP RESTful Application Programming Model (RAP).
        Your task is to analyze the provided ABAP code chunk and generate a detailed, structured summary in Markdown format.

        **Context:**
        - File Name: {file_name}
        - Object Type Hint: {chunk_type}
        - Chunk: {chunk_index} of {total_chunks}

        **ABAP Code Chunk:**
        ```abap
        {chunk_content}
        ```

        **Instructions:**
        Analyze the code to identify the precise ABAP object type and provide a structured summary. Your primary goal is to adapt the format of the 'Detailed Breakdown' section to accurately and clearly represent the specific type of ABAP object provided. If certain information is not present in this chunk, state that clearly.

        ---

        **1. Object Identification and Purpose:**
        - **Identified Object Type:** (e.g., Global Class, Function Group, Report Program, Behavior Definition, Data Definition/CDS View, Database Table)
        - **Purpose:** Briefly describe the main purpose of this object. What business or technical process does it implement?

        ---

        **2. Technical Analysis:**
        - **Database Interaction:** List the database tables/CDS views accessed and the type of operations performed (e.g., SELECT from SFLIGHT, UPDATE on /DMO/TRAVEL, EML call to modify Travel).
        - **Key Components:** Identify the main components or logic blocks (e.g., Methods of a class, Forms in a report, Function Modules in a group, Actions in a BDEF, Selection-screen elements).
        - **Dependencies & Calls:** List any significant external dependencies called from this code (e.g., other classes, function modules, APIs, CDS Views).
        - **Programming Model/Pattern (if applicable):** If a specific design pattern or model is evident (e.g., RAP Managed/Unmanaged, ALV Report, Singleton Class, BAPI), please identify it.

        ---

        **3. Object-Specific Detailed Breakdown:**
        Based on the identified object type, provide a detailed breakdown using the most appropriate format from the examples below. If the object type is not listed, create a similar, logical structure. Populate the table(s) with all relevant components found in the code chunk.

        * **Example for a Class / Function Module / BAPI / Exit:**
            | Component Name | Type (Method, FM) | Description of Logic | Parameters (Importing, Changing) | Parameters (Exporting, Returning) | Exceptions |
            |---|---|---|---|---|---|
            | `GET_TRAVEL_DATA` | `Method` | Retrieves travel data based on key. | `it_travel_keys` | `rt_travel_data` | `cx_some_exception`|

        * **Example for a Database Table / Data Definition (CDS View):**
            | Field / Element Name | Key | Data Element / Type | Description / Annotations |
            |---|---|---|---|
            | `MANDT` | **Yes** | `MANDT` | Client |
            | `TRAVEL_ID` | **Yes** | `/DMO/TRAVEL_ID` | Travel ID |
            | `AGENCY_ID` | No | `/DMO/AGENCY_ID` | Agency ID |
            | `BeginDate` | No | `@Semantics.businessDate.from` `Dats` | Start Date of Travel |

        * **Example for a Behavior Definition (BDEF) or Projection:**
            | Keyword | Component Name | Details / Signature |
            |---|---|---|
            | `define behavior for` | `ZI_MY_TRAVEL` | `alias Travel` |
            | `action` | `acceptTravel` | `result [1] $self` |
            | `determination`| `setTravelStatus` | `on modify` |
            | `validation` | `validateDates` | `on save` |
            | `field` | `TravelID` | `( readonly )` |
            
        * **Example for a Report Program:**
            | Component | Type | Description / Details |
            |---|---|---|
            | `p_carrid` | `PARAMETER` | Selection for Carrier ID. `TYPE s_carr_id`. |
            | `s_connid` | `SELECT-OPTIONS` | Selection for Connection ID. `FOR sflight-connid`.|
            | `INITIALIZATION` | `EVENT` | Sets default values for the selection screen. |
            | `START-OF-SELECTION`|`EVENT` | Main data retrieval and processing logic starts here. |
            | `PERFORM display_data` |`SUBROUTINE`| Calls the form routine to display the ALV grid. |

        * **Example for a BAdI Definition/Implementation:**
            **BAdI:** `BADI_MY_EXAMPLE`
            - **Description:** BAdI to enhance the booking process.
            - **Interface:** `IF_EX_MY_EXAMPLE_BADI`
                | Method Name | Description | Parameters (Importing, Changing) | Parameters (Exporting, Returning) |
                |---|---|---|---|
                | `VALIDATE_BOOKING`| Validates extra fields. | `is_booking_data` | `ct_return_messages` |

        Generate a comprehensive yet concise response based *only* on the provided code chunk.
        """)
