import re
from langchain_core.documents.base import Document
from typing import Any, ClassVar, Dict, List, Self


class Prompt:
    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super(Prompt, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized: bool = True
            # Configuration for prompt optimization
            self._max_code_length: int = 16384  # Increased for better handling of ABAP files
            self._priority_sections: List[str] = [
                "Document Information",
                "Overview",
                "Object Structure",
                "Method/Function Specifications",
                "Business Logic",
                "Dependencies",
            ]
            # ABAP-specific keywords for prioritization
            self._abap_critical_keywords: List[str] = [
                "CLASS",
                "ENDCLASS",
                "METHOD",
                "ENDMETHOD",
                "DEFINE",
                "SELECT",
                "TYPES",
                "DATA",
                "INTERFACE",
                "ENDINTERFACE",
                "FORM",
                "ENDFORM",
                "FUNCTION",
                "ENDFUNCTION",
                "MODULE",
                "ENDMODULE",
                "BEHAVIOR",
                "PROJECTION",
                "VIEW",
                "ENTITY",
            ]

    def get_prompt_technical_specification(
        self,
        code: List[Document],
        spec: List[Document],
        mode: str,  # Options: "core", "comprehensive", "segmented"
    ) -> str:
        """
        Generate optimized prompt based on selected mode

        Args:
            code: List of code documents
            spec: List of specification template documents
            mode: Processing mode - "core", "comprehensive", "segmented"
        """
        code_content: str = self._extract_and_optimize_code(documents=code)
        spec_content: str = self._extract_spec_from_documents(documents=spec)

        if mode == "comprehensive":
            return self._get_comprehensive_prompt(code_content=code_content, spec_content=spec_content)
        else:
            raise ValueError(f"Unsupported mode: {mode}. Supported modes are: 'comprehensive'.")

    def _extract_and_optimize_code(self, documents: List[Document]) -> str:
        """Extract and optimize code content with improved ABAP-aware processing"""
        if not documents:
            return ""

        # First pass: analyze all documents to understand their importance and size
        document_metadata = self._analyze_documents(documents)

        # Second pass: process documents based on priority and available space
        code_sections: List[str] = []
        total_length = 0
        processed_count = 0

        # Sort documents by priority (critical ABAP structures first)
        sorted_docs = sorted(enumerate(documents), key=lambda x: document_metadata[x[0]]["priority_score"], reverse=True)

        for original_index, code in sorted_docs:
            if not hasattr(code, "page_content") or not code.page_content:
                continue

            content: str = code.page_content.strip()
            if not content:
                continue

            metadata = document_metadata[original_index]
            section_header = f"--- Code Section {original_index + 1}: {metadata['filename']} ---"

            # Calculate space needed for this section
            estimated_section_size = len(section_header) + len(content) + 20  # Buffer for formatting

            # Check if we can fit the entire section
            if total_length + estimated_section_size <= self._max_code_length:
                # Full section fits
                section_content = f"{section_header}\n{content}\n"
                code_sections.append(section_content)
                total_length += len(section_content)
                processed_count += 1
            else:
                # Need to truncate or skip
                remaining_space = self._max_code_length - total_length - len(section_header) - 100  # Buffer

                if remaining_space > 200:  # Only truncate if we have meaningful space
                    truncated_content = self._truncate_code_section_improved(content, remaining_space, metadata["structure_info"])
                    section_content = f"{section_header}\n{truncated_content}\n"
                    code_sections.append(section_content)
                    total_length += len(section_content)
                    processed_count += 1

                # Stop processing as we're near the limit
                break

        # Add summary of processing
        summary = f"\n--- Processing Summary ---\nProcessed {processed_count}/{len(documents)} code sections\n"
        if processed_count < len(documents):
            skipped = len(documents) - processed_count
            summary += f"Skipped {skipped} sections due to size constraints\n"

        result = "\n".join(code_sections) + summary
        return result

    def _analyze_documents(self, documents: List[Document]) -> Dict[int, Dict[str, Any]]:
        """Analyze documents to determine processing priority and structure info"""
        metadata = {}

        for index, document in enumerate(documents):
            if not hasattr(document, "page_content") or not document.page_content:
                metadata[index] = {"filename": f"Document_{index + 1}", "size": 0, "priority_score": 0, "structure_info": {}}
                continue

            content = document.page_content.strip()

            # Extract filename from metadata if available
            filename = f"Document_{index + 1}"
            if hasattr(document, "metadata") and "source" in document.metadata:
                filename = document.metadata["source"]

            # Calculate priority score based on ABAP keywords and structures
            priority_score = self._calculate_priority_score(content)

            # Analyze structure for smart truncation
            structure_info = self._analyze_abap_structure(content)

            metadata[index] = {
                "filename": filename,
                "size": len(content),
                "priority_score": priority_score,
                "structure_info": structure_info,
            }

        return metadata

    def _calculate_priority_score(self, content: str) -> int:
        """Calculate priority score for ABAP code based on keywords and patterns"""
        score = 0
        content_upper = content.upper()

        # High priority patterns
        high_priority_patterns = {
            r"\bCLASS\s+\w+\s+DEFINITION\b": 50,
            r"\bCLASS\s+\w+\s+IMPLEMENTATION\b": 45,
            r"\bINTERFACE\s+\w+": 40,
            r"\bMETHOD\s+\w+": 20,
            r"\bDEFINE\s+BEHAVIOR\b": 35,
            r"\bDEFINE\s+ROOT\s+VIEW\s+ENTITY\b": 30,
            r"\bSELECT\s+": 15,
            r"\bTYPES:\s*": 25,
        }

        for pattern, points in high_priority_patterns.items():
            matches = re.findall(pattern, content_upper)
            score += len(matches) * points

        # Bonus for critical ABAP keywords
        for keyword in self._abap_critical_keywords:
            count = content_upper.count(keyword)
            score += count * 5

        # Penalty for very short files (likely config/metadata only)
        if len(content) < 200:
            score = max(0, score - 20)

        return score

    def _analyze_abap_structure(self, content: str) -> Dict[str, Any]:
        """Analyze ABAP code structure for intelligent processing"""
        lines = content.split("\n")
        structure_info = {
            "class_definitions": [],
            "method_signatures": [],
            "important_lines": [],
            "comment_lines": [],
            "total_lines": len(lines),
        }

        for i, line in enumerate(lines):
            line_upper = line.strip().upper()

            # Track class definitions
            if re.match(r"\s*CLASS\s+\w+\s+(DEFINITION|IMPLEMENTATION)", line_upper):
                structure_info["class_definitions"].append(i)

            # Track method signatures
            elif re.match(r"\s*METHODS?\s*:", line_upper) or re.match(r"\s*METHOD\s+\w+", line_upper):
                structure_info["method_signatures"].append(i)

            # Track important structural lines
            elif any(keyword in line_upper for keyword in self._abap_critical_keywords):
                structure_info["important_lines"].append(i)

            # Track comments
            elif line.strip().startswith("*") or line.strip().startswith('"'):
                structure_info["comment_lines"].append(i)

        return structure_info

    def _truncate_code_section_improved(self, content: str, max_length: int, structure_info: Dict[str, Any]) -> str:
        """Intelligently truncate ABAP code while preserving critical structures"""
        if len(content) <= max_length:
            return content

        lines = content.split("\n")
        preserved_lines = []
        current_length = 0

        # Priority order for line preservation
        priority_line_indices = set()

        # Highest priority: class definitions and method signatures
        priority_line_indices.update(structure_info.get("class_definitions", []))
        priority_line_indices.update(structure_info.get("method_signatures", []))

        # High priority: other important structural lines
        priority_line_indices.update(structure_info.get("important_lines", []))

        # Process priority lines first
        for i in sorted(priority_line_indices):
            if i < len(lines):
                line = lines[i]
                if current_length + len(line) + 1 < max_length * 0.7:  # Reserve space for other content
                    preserved_lines.append((i, line))
                    current_length += len(line) + 1

        # Fill remaining space with other significant lines
        remaining_space = max_length - current_length
        used_indices = {i for i, _ in preserved_lines}

        for i, line in enumerate(lines):
            if i in used_indices or i in structure_info.get("comment_lines", []):
                continue

            if current_length + len(line) + 1 < remaining_space:
                preserved_lines.append((i, line))
                current_length += len(line) + 1
            else:
                break

        # Sort by original line order and reconstruct
        preserved_lines.sort(key=lambda x: x[0])

        if preserved_lines:
            result_lines = []
            last_index = -1

            for line_index, line in preserved_lines:
                if line_index > last_index + 1:
                    result_lines.append(f"... [Lines {last_index + 1}-{line_index - 1} omitted] ...")
                result_lines.append(line)
                last_index = line_index

            result = "\n".join(result_lines)
        else:
            # Fallback: take first portion
            result = content[: max_length - 100]
            if "\n" in result:
                result = result[: result.rfind("\n")]

        # Add truncation notice
        original_lines = len(lines)
        preserved_count = len(preserved_lines)
        result += f"\n\n... [Content truncated: {preserved_count}/{original_lines} lines preserved, {len(content)} -> {len(result)} chars]"

        return result

    def _get_comprehensive_prompt(self, code_content: str, spec_content: str) -> str:
        return f"""
CONTEXT: You are an experienced SAP ABAP technical consultant with 10+ years of experience creating enterprise-grade technical documentation for RAP (RESTFUL ABAP Programming) applications.

OBJECTIVE: Create a comprehensive Technical Specification document for the provided ABAP code following industry best practices for SAP RAP applications.

CODE SECTIONS TO ANALYZE:
{code_content}

TEMPLATE TO FOLLOW:
{spec_content}

SPECIFIC REQUIREMENTS:
1. Identify and document the RAP architecture layers (Business Object, Projection, Service)
2. Document behavior definitions and implementations
3. Explain CDS view relationships and annotations
4. Detail the unmanaged implementation pattern used
5. Document API class functionality and data flow
6. Include UI annotations and metadata extensions

DELIVERABLE: Complete technical specification document following the provided template structure with specific focus on RAP architectural patterns and enterprise ABAP development practices.
"""

    def _extract_spec_from_documents(self, documents: List[Document]) -> str:
        """Extract specification template content"""
        if not documents:
            return "No specification template provided."

        spec_sections: List[str] = []
        for i, spec in enumerate(documents):
            if hasattr(spec, "page_content") and spec.page_content:
                content: str = spec.page_content.strip()
                if content:
                    spec_sections.append(f"--- Template Section {i + 1} ---\n{content}\n")

        return "\n".join(spec_sections) if spec_sections else "No valid specification content found."
