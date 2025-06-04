
# Technical Specification: [Program Name - LLM to infer or use ABAP filename]

## 1. General Information
- **Program ID/Name**: `[LLM to infer from REPORT statement or filename]`
- **ABAP Type**: `(e.g., Report, Module Pool, Function Group, Class, Include)` `[LLM to infer]`
- **Title/Description**: `[LLM to infer from comments or REPORT statement title]`
- **Creation/Last Change Date**: `[If available in comments, otherwise N/A]`
- **Author**: `[If available in comments, otherwise N/A]`

## 2. Purpose & Overview
- **Main Objective**: `[LLM to describe the primary goal of the ABAP program based on its logic and comments]`
- **Key Functionalities**:
  - `[LLM to list major operations performed, e.g., data extraction, data update, report generation, user interaction]`

## 3. Program Objects & Declarations
### 3.1. Database Tables Accessed
- `[Table Name 1]`: `(SELECT/UPDATE/INSERT/DELETE)` `[Purpose/Fields accessed, if discernible]`
- `[Table Name 2]`: `(SELECT/UPDATE/INSERT/DELETE)` `[Purpose/Fields accessed, if discernible]`
  *(List all significant DB tables and the type of access)*

### 3.2. Key Internal Tables & Structures
- `[Internal Table/Structure Name 1]`: `[Type definition (e.g., LIKE, TYPE), Key Fields, Purpose in the program]`
- `[Internal Table/Structure Name 2]`: `[Type definition, Key Fields, Purpose]`

### 3.3. Selection Screen (If applicable - for Reports, Module Pools with selection screens)
- **Parameters**:
  - `P_[Parameter Name]`: `[TYPE, OBLIGATORY/OPTIONAL, DEFAULT value, Associated dictionary object (LIKE), Description/Purpose]`
- **Select-Options**:
  - `S_[Select-Option Name]`: `[FOR Field, Associated dictionary object, Description/Purpose]`

### 3.4. Important Global Variables & Constants
- `[Variable Name (g_variable, gr_object, etc.)]`: `[TYPE, Purpose/Role in program]`
- `[Constant Name (gc_constant)]`: `[VALUE, Purpose]`

## 4. Program Logic & Flow
### 4.1. Initialization (`INITIALIZATION`, `LOAD-OF-PROGRAM`, Constructor for classes)
- `[Describe logic performed during initialization, e.g., default values, object instantiation]`

### 4.2. Main Processing Events (e.g., `START-OF-SELECTION`, `AT SELECTION-SCREEN`, PBO/PAI modules, Methods)
- **`[Event/Block Name 1 e.g., START-OF-SELECTION]`**:
  - `[Describe main data retrieval, core business logic, calculations, and processing steps within this block]`
- **`[Event/Block Name 2 e.g., PAI Module USER_COMMAND_0100]`**:
  - `[Describe user command handling, screen field validation, subsequent actions]`

### 4.3. Key Subroutines (FORMs) / Methods (of local/global CLASSes)
#### 4.3.1. `[FORM/METHOD Name 1]`
- **Purpose**: `[Brief description of what this routine/method does]`
- **Key Logic Steps**: `[Summarize the main steps or algorithms inside]`
- **Input Parameters (USING/IMPORTING)**: `[List parameters and their types/purpose]`
- **Output/Changing Parameters (CHANGING/EXPORTING/RETURNING)**: `[List parameters and their types/purpose]`

#### 4.3.2. `[FORM/METHOD Name 2]`
  *(Repeat structure for other significant routines/methods)*

### 4.4. Called Function Modules (Standard or Custom)
- `[Function Module Name 1 (e.g., READ_TEXT, ALV_GRID_DISPLAY)]`:
  - **Purpose**: `[Why this FM is called]`
  - **Key Import/Export/Table Parameters Used**: `[List important parameters passed or received]`
- `[Function Module Name 2]`:
  *(Repeat for other significant FMs)*

### 4.5. Output & Display Logic (e.g., `WRITE` statements, ALV, SmartForms/Adobe Forms calls)
- `[Describe how the output is generated and presented to the user. If ALV, mention key fields displayed or layout characteristics if inferable.]`

## 5. Error Handling & Messaging
- `[Describe how errors are caught (e.g., SY-SUBRC checks, TRY-CATCH blocks) and reported (e.g., MESSAGE E..., MESSAGE W...)]`
- `[List key message classes/numbers used if discernible]`

## 6. Authorization Checks (If discernible)
- `[AUTHORITY-CHECK OBJECT 'object_name' ID 'id_name' FIELD field_value]`: `[Brief description of the check]`
  *(List any explicit authority checks found)*

## 7. Performance Considerations (If any obvious from code)
- `[e.g., Use of specific index hints, FOR ALL ENTRIES, handling of large internal tables, parallel processing calls, etc. Note if no specific optimizations are apparent.]`

## 8. Assumptions & Notes by AI
- `[LLM can add notes about its analysis, parts of the code it found ambiguous, or assumptions made during generation.]`
