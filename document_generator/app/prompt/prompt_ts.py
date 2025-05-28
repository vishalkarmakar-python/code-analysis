from langchain_core.documents.base import Document
from typing import ClassVar, List, Self


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
            self._max_code_length: int = 15000  # Adjust based on your LLM's context window
            self._priority_sections: List[str] = [
                "Document Information",
                "Overview",
                "Object Structure",
                "Method/Function Specifications",
                "Business Logic",
                "Dependencies",
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
        code_content: str = self._extract_and_optimize_code(code)

        if mode == "comprehensive":
            return self._get_comprehensive_prompt(code_content, spec)
        else:
            raise ValueError(f"Unsupported mode: {mode}. Supported modes are: 'comprehensive'.")

    def _extract_and_optimize_code(self, documents: List[Document]) -> str:
        """Extract and optimize code content with length management"""
        code_sections: List[str] = []
        total_length = 0

        for i, code in enumerate(documents):
            if hasattr(code, "page_content") and code.page_content:
                content: str = code.page_content.strip()
                if content:
                    # Check if adding this section would exceed limit
                    section_content: str = f"--- Code Section {i + 1} ---\n{content}\n"

                    if total_length + len(section_content) > self._max_code_length:
                        # Truncate or summarize this section
                        truncated_content: str = self._truncate_code_section(content, self._max_code_length - total_length)
                        section_content = f"--- Code Section {i + 1} (Truncated) ---\n{truncated_content}\n"

                    code_sections.append(section_content)
                    total_length += len(section_content)

                    if total_length >= self._max_code_length:
                        break

        return "\n".join(code_sections)

    def _truncate_code_section(self, content: str, max_length: int) -> str:
        """Intelligently truncate code section while preserving key information"""
        if len(content) <= max_length:
            return content

        # Try to preserve important parts like class definitions, method signatures
        lines: List[str] = content.split("\n")
        important_lines: List[str] = []
        current_length = 0

        for line in lines:
            # Prioritize lines with key ABAP keywords
            if any(keyword in line.upper() for keyword in ["CLASS", "METHOD", "DEFINE", "SELECT", "TYPES", "DATA"]):
                if current_length + len(line) < max_length:
                    important_lines.append(line)
                    current_length += len(line) + 1
            elif current_length + len(line) < max_length * 0.8:  # Fill remaining with other lines
                important_lines.append(line)
                current_length += len(line) + 1

        result = "\n".join(important_lines)
        if len(result) < len(content):
            result += f"\n\n... [Content truncated. Original length: {len(content)} chars]"

        return result

    def _get_comprehensive_prompt(self, code_content: str, spec: List[Document]) -> str:
        """Generate full comprehensive prompt"""
        spec_content: str = self._extract_spec_from_documents(spec)

        return f"""
                    CONTEXT: You are an experienced SAP ABAP technical consultant with 10 years of experience creating enterprise-grade technical documentation.

                    OBJECTIVE: Create a comprehensive Technical Specification document for the provided ABAP code following industry best practices.

                    INSTRUCTIONS:
                    1. Analyze code systematically and thoroughly
                    2. Follow the provided template structure exactly
                    3. Ensure technical accuracy and completeness
                    4. Use professional documentation standards

                    CODE SECTIONS TO ANALYZE:
                    {code_content}

                    PROCESSING APPROACH:
                    1. First, understand the overall application structure
                    2. Identify key business objects (Travel, Booking entities)
                    3. Analyze RAP behavior definitions and implementations
                    4. Document CDS views and database relationships
                    5. Map UI annotations and service definitions

                    TEMPLATE TO FOLLOW:
                    {spec_content}

                    QUALITY REQUIREMENTS:
                    - Technical accuracy is paramount
                    - Include all relevant code patterns and designs
                    - Explain business context and purpose
                    - Document integration points and dependencies
                    - Provide clear examples where helpful

                    DELIVERABLE: Complete technical specification document following the provided template structure.
                """

    def _extract_spec_from_documents(self, documents: List[Document]) -> str:
        """Extract specification template content"""
        spec_sections: List[str] = []
        for i, spec in enumerate(documents):
            if hasattr(spec, "page_content") and spec.page_content:
                content: str = spec.page_content.strip()
                if content:
                    spec_sections.append(f"--- Template Section {i + 1} ---\n{content}\n")

        return "\n".join(spec_sections)


# from langchain_core.documents.base import Document
# from typing import ClassVar, List, Self

# class Prompt:
#     _instance: ClassVar[Self | None] = None

#     def __new__(cls) -> Self:
#         if cls._instance is None:
#             cls._instance = super(Prompt, cls).__new__(cls)
#         return cls._instance

#     def __init__(self) -> None:
#         # Only initialize attributes if this is the first time __init__ is called
#         if not hasattr(self, "_initialized"):
#             self._initialized: bool = True

#     def get_prompt_technical_specification(self, code: List[Document], spec: List[Document]) -> str:
#         code_pages: str = self._extract_code_from_documents(code)
#         spec_pages: str = self._extract_spec_from_documents(spec)
#         return f"""
#             Context
#             You are an experienced SAP ABAP developer with 10 years of experience and great in writing technical specification writing.
#             You are tasked with creating a comprehensive Technical Specification document for the below code files.
#             {code_pages}
#             Use the provided {spec_pages} template to generate detailed technical documentation that covers the entire application.
#             """

#     def _extract_code_from_documents(self, documents: List[Document]) -> str:
#         """Extract and prepare code content from documents for AI processing"""
#         code_sections: List[str] = []
#         for i, code in enumerate(documents):
#             if hasattr(code, "page_content") and code.page_content:
#                 content: str = code.page_content.strip()
#                 if content:
#                     # Add section separator for better AI parsing
#                     code_sections.append(f"--- Code Section {i + 1} ---\n{content}\n")

#         # Set the combined content to prompt_template
#         code_template: str = "\n".join(code_sections)
#         return code_template

#     def _extract_spec_from_documents(self, documents: List[Document]) -> str:
#         """Extract and prepare code content from documents for AI processing"""
#         spec_sections: List[str] = []
#         for i, spec in enumerate(documents):
#             if hasattr(spec, "page_content") and spec.page_content:
#                 content: str = spec.page_content.strip()
#                 if content:
#                     # Add section separator for better AI parsing
#                     spec_sections.append(f"--- Code Section {i + 1} ---\n{content}\n")

#         # Set the combined content to prompt_template
#         spec_template: str = "\n".join(spec_sections)
#         return spec_template
