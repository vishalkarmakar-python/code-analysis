from langchain_core.documents.base import Document
from langchain_core.prompts import PromptTemplate
from typing import Any, Dict, List, Optional


class PromptGenerator:
    """
    Generate dynamic prompts for gemma3:4b model to create technical specification documents
    from ABAP code using context-preserved chunks and markdown specification templates.
    """

    # Enhanced template for ABAP + Markdown specification generation
    ENHANCED_TECHNICAL_SPEC_TEMPLATE: str = """
        You are an expert ABAP developer and technical documentation specialist. 
        Your task is to generate a comprehensive technical specification document based on the provided ABAP code and specification template.

        ## Context Information
        - Model: gemma3:4b (Ollama via ChatOllama)
        - Document Type: Technical Specification
        - Template Type: {template_type}
        - Processing Mode: {processing_mode}
        - Source Information: {source_info}

        ## Specification Template Reference
        {template_reference}

        ## Document Analysis
        {document_analysis}

        ## ABAP Code Content
        {abap_code_content}

        ## Specification Template Content
        {spec_template_content}

        ## Generation Requirements
        Using the provided specification template as a guide, generate a technical specification document that includes:

        ### 1. Document Overview
        - Purpose and functional description based on ABAP code analysis
        - System/module context derived from code structure
        - Key business objectives identified from code logic

        ### 2. Technical Architecture  
        - Component structure and relationships found in the code
        - Data flow and processing logic from ABAP implementation
        - Integration points and interfaces discovered in code

        ### 3. Implementation Details
        - Method and class descriptions from ABAP code
        - Data structures and type definitions
        - Algorithm explanations and business rules implementation

        ### 4. Data Management
        - Database operations and SQL usage patterns
        - Data validation and transformation logic
        - Input/output specifications from code analysis

        ### 5. Error Handling & Validation
        - Exception handling mechanisms implemented
        - Input validation rules found in code
        - Error recovery procedures identified

        ### 6. Performance & Security
        - Performance considerations from code analysis
        - Security measures and authorization checks
        - Resource usage patterns observed

        ### 7. Dependencies & Integration
        - External system connections discovered
        - API calls and web services usage
        - File operations and interfaces found

        ## Output Instructions
        - Follow the structure and format suggested by the specification template
        - Write in clear, professional technical language
        - Follow standard ABAP documentation conventions
        - Include relevant code snippets and references from the provided ABAP code
        - Organize content logically with proper headings as shown in template
        - Ensure completeness and maintainability
        - Map ABAP code elements to appropriate template sections
        - {additional_instructions}

        ## Additional Context
        {additional_context}

        Based on the provided ABAP code and using the specification template as a structural guide, generate the technical specification document now:"""

    @staticmethod
    def create_enhanced_prompt() -> PromptTemplate:
        """
        Create an enhanced prompt template that handles both ABAP code and markdown specifications.

        Returns:
            PromptTemplate configured for ABAP + Markdown processing
        """
        prompt = PromptTemplate(
            input_variables=[
                "template_type",
                "processing_mode",
                "source_info",
                "template_reference",
                "document_analysis",
                "abap_code_content",
                "spec_template_content",
                "additional_instructions",
                "additional_context",
            ],
            template=PromptGenerator.ENHANCED_TECHNICAL_SPEC_TEMPLATE,
        )

        return prompt

    @staticmethod
    def prepare_enhanced_prompt_inputs(
        abap_documents: List[Document],
        markdown_documents: List[Document],
        template_type: str = "abap_technical_specification",
        additional_context: str = "",
        additional_instructions: str = "",
    ) -> Dict[str, Any]:
        """
        Prepare input variables for the enhanced prompt from both ABAP and markdown document chunks.

        Args:
            abap_documents: List of ABAP code document chunks
            markdown_documents: List of markdown specification template chunks
            template_type: Type of template being used
            additional_context: Any additional context information
            additional_instructions: Specific generation instructions

        Returns:
            Dictionary with prepared input variables
        """

        if not abap_documents and not markdown_documents:
            raise ValueError("No documents provided for processing")

        # Determine processing mode
        abap_count = len(abap_documents) if abap_documents else 0
        markdown_count = len(markdown_documents) if markdown_documents else 0
        processing_mode = f"ABAP Chunks: {abap_count}, Template Chunks: {markdown_count}"

        # Build source information
        source_info = PromptGenerator._build_combined_source_info(abap_documents, markdown_documents)

        # Build template reference
        template_reference = PromptGenerator._build_template_reference(markdown_documents)

        # Build comprehensive document analysis
        document_analysis = PromptGenerator._build_combined_document_analysis(abap_documents, markdown_documents)

        # Build ABAP code content
        abap_code_content = PromptGenerator._build_abap_code_content(abap_documents) if abap_documents else "No ABAP code provided"

        # Build specification template content
        spec_template_content = (
            PromptGenerator._build_spec_template_content(markdown_documents) if markdown_documents else "No specification template provided"
        )

        # Set default additional instructions
        if not additional_instructions:
            instructions = []
            if abap_count > 1:
                instructions.append("Integrate information from multiple ABAP code chunks")
            if markdown_count > 1:
                instructions.append("Synthesize multiple specification templates")
            if abap_count > 0 and markdown_count > 0:
                instructions.append("Map ABAP code elements to specification template structure")

            additional_instructions = "; ".join(instructions) if instructions else "Generate comprehensive technical specification"

        return {
            "template_type": template_type,
            "processing_mode": processing_mode,
            "source_info": source_info,
            "template_reference": template_reference,
            "document_analysis": document_analysis,
            "abap_code_content": abap_code_content,
            "spec_template_content": spec_template_content,
            "additional_instructions": additional_instructions,
            "additional_context": additional_context,
        }

    @staticmethod
    def generate_enhanced_prompt(
        abap_documents: List[Document],
        markdown_documents: List[Document],
        template_type: str = "abap_technical_specification",
        additional_context: str = "",
        additional_instructions: str = "",
    ) -> str:
        """
        Generate a formatted prompt for both ABAP code and markdown specification documents.

        Args:
            abap_documents: List of ABAP code document chunks
            markdown_documents: List of markdown specification template chunks
            template_type: Type of template being used
            additional_context: Any additional context information
            additional_instructions: Specific generation instructions

        Returns:
            Formatted prompt string ready for ChatOllama with gemma3:4b
        """

        # Create the enhanced prompt
        prompt: PromptTemplate = PromptGenerator.create_enhanced_prompt()

        # Prepare input variables
        inputs: Dict[str, Any] = PromptGenerator.prepare_enhanced_prompt_inputs(
            abap_documents=abap_documents,
            markdown_documents=markdown_documents,
            template_type=template_type,
            additional_context=additional_context,
            additional_instructions=additional_instructions,
        )

        # Format and return the prompt
        return prompt.format(**inputs)

    @staticmethod
    def _build_combined_source_info(abap_documents: List[Document], markdown_documents: List[Document]) -> str:
        """Build combined source information from both document types."""
        info_parts = []

        if abap_documents:
            abap_sources = set(doc.metadata.get("source", "unknown") for doc in abap_documents)
            abap_doc_ids = set(doc.metadata.get("document_id", "unknown") for doc in abap_documents)
            info_parts.append(f"ABAP Sources: {', '.join(abap_sources)}")
            info_parts.append(f"ABAP Document IDs: {', '.join(abap_doc_ids)}")
            info_parts.append(f"ABAP Chunks: {len(abap_documents)}")

        if markdown_documents:
            md_sources = set(doc.metadata.get("source", "unknown") for doc in markdown_documents)
            md_doc_ids = set(doc.metadata.get("document_id", "unknown") for doc in markdown_documents)
            info_parts.append(f"Template Sources: {', '.join(md_sources)}")
            info_parts.append(f"Template Document IDs: {', '.join(md_doc_ids)}")
            info_parts.append(f"Template Chunks: {len(markdown_documents)}")

        return "\n".join(info_parts)

    @staticmethod
    def _build_template_reference(markdown_documents: List[Document]) -> str:
        """Build template reference information."""
        if not markdown_documents:
            return "No specification template available - generate using standard ABAP documentation format"

        ref_parts = []
        ref_parts.append(f"Available Templates: {len(markdown_documents)} specification documents")

        # Analyze template structure
        all_content = ""
        for doc in markdown_documents:
            all_content += PromptGenerator._clean_code_content(doc.page_content) + "\n"

        # Look for common markdown structures
        headers = all_content.count("#")
        if headers > 0:
            ref_parts.append(f"Template Structure: {headers} headers found")

        ref_parts.append("Use these templates as structural and formatting guidelines for the output")

        return "\n".join(ref_parts)

    @staticmethod
    def _build_combined_document_analysis(abap_documents: List[Document], markdown_documents: List[Document]) -> str:
        """Build comprehensive analysis of both ABAP and markdown documents."""
        analysis_parts = []

        # ABAP Analysis
        if abap_documents:
            analysis_parts.append("=== ABAP Code Analysis ===")
            abap_analysis = PromptGenerator._analyze_abap_documents(abap_documents)
            analysis_parts.append(abap_analysis)

        # Template Analysis
        if markdown_documents:
            analysis_parts.append("=== Specification Template Analysis ===")
            template_analysis = PromptGenerator._analyze_template_documents(markdown_documents)
            analysis_parts.append(template_analysis)

        return "\n\n".join(analysis_parts)

    @staticmethod
    def _analyze_abap_documents(abap_documents: List[Document]) -> str:
        """Analyze ABAP documents for code elements."""
        total_chars = sum(len(PromptGenerator._clean_code_content(doc.page_content)) for doc in abap_documents)

        # Combine all ABAP content for analysis
        all_content = ""
        for doc in abap_documents:
            all_content += PromptGenerator._clean_code_content(doc.page_content) + "\n"

        abap_elements = []

        # Analyze ABAP constructs
        constructs = {
            "Classes": all_content.count("CLASS"),
            "Methods": all_content.count("METHOD"),
            "Interfaces": all_content.count("INTERFACE"),
            "Function Modules": all_content.count("FUNCTION"),
            "Form Routines": all_content.count("FORM"),
            "SQL Operations": all_content.count("SELECT"),
            "Reports": all_content.count("REPORT"),
        }

        for construct, count in constructs.items():
            if count > 0:
                abap_elements.append(f"{construct}: {count}")

        analysis = [f"Total ABAP Content: {total_chars} characters"]
        if abap_elements:
            analysis.append(f"ABAP Elements: {', '.join(abap_elements)}")

        return "\n".join(analysis)

    @staticmethod
    def _analyze_template_documents(markdown_documents: List[Document]) -> str:
        """Analyze markdown template documents."""
        total_chars = sum(len(PromptGenerator._clean_code_content(doc.page_content)) for doc in markdown_documents)

        # Combine all template content
        all_content = ""
        for doc in markdown_documents:
            all_content += PromptGenerator._clean_code_content(doc.page_content) + "\n"

        # Analyze markdown structure
        structure_elements = []

        headers = all_content.count("#")
        if headers > 0:
            structure_elements.append(f"Headers: {headers}")

        tables = all_content.count("|")
        if tables > 5:  # Likely contains tables
            structure_elements.append("Contains tables")

        code_blocks = all_content.count("```")
        if code_blocks > 0:
            structure_elements.append(f"Code blocks: {code_blocks // 2}")

        analysis = [f"Total Template Content: {total_chars} characters"]
        if structure_elements:
            analysis.append(f"Template Elements: {', '.join(structure_elements)}")

        return "\n".join(analysis)

    @staticmethod
    def _build_spec_template_content(markdown_documents: List[Document]) -> str:
        """Build formatted specification template content."""
        if not markdown_documents:
            return "No specification template content available"

        if len(markdown_documents) == 1:
            # Single template - return clean content
            return f"```markdown\n{PromptGenerator._clean_code_content(markdown_documents[0].page_content)}\n```"

        # Multiple templates - organize by document
        content_parts = []

        # Group by document ID
        doc_groups = {}
        for doc in markdown_documents:
            doc_id = doc.metadata.get("document_id", "unknown")
            if doc_id not in doc_groups:
                doc_groups[doc_id] = []
            doc_groups[doc_id].append(doc)

        # Format each template group
        for doc_id, doc_chunks in doc_groups.items():
            sorted_chunks = sorted(doc_chunks, key=lambda x: x.metadata.get("chunk_index", 0))

            if len(doc_groups) > 1:
                content_parts.append(f"## Template: {doc_id}")

            for i, chunk in enumerate(sorted_chunks):
                if len(sorted_chunks) > 1:
                    chunk_info = f"Section {i + 1}/{len(sorted_chunks)}"
                    content_parts.append(f"### {chunk_info}")

                clean_content = PromptGenerator._clean_code_content(chunk.page_content)
                content_parts.append(f"```markdown\n{clean_content}\n```")

        return "\n\n".join(content_parts)

    @staticmethod
    def _build_abap_code_content(abap_documents: List[Document]) -> str:
        """Build formatted ABAP code content from chunks."""
        if not abap_documents:
            return "No ABAP code content available"

        if len(abap_documents) == 1:
            # Single chunk - return clean content
            return f"```abap\n{PromptGenerator._clean_code_content(abap_documents[0].page_content)}\n```"

        # Multiple chunks - organize by document and chunk
        content_parts = []

        # Group by document ID
        doc_groups = {}
        for doc in abap_documents:
            doc_id = doc.metadata.get("document_id", "unknown")
            if doc_id not in doc_groups:
                doc_groups[doc_id] = []
            doc_groups[doc_id].append(doc)

        # Format each document group
        for doc_id, doc_chunks in doc_groups.items():
            sorted_chunks = sorted(doc_chunks, key=lambda x: x.metadata.get("chunk_index", 0))

            if len(doc_groups) > 1:
                content_parts.append(f"## ABAP Document: {doc_id}")

            for i, chunk in enumerate(sorted_chunks):
                metadata = chunk.metadata
                if len(sorted_chunks) > 1:
                    chunk_info = f"Chunk {metadata.get('chunk_index', i) + 1}/{metadata.get('total_chunks', len(sorted_chunks))}"
                    content_parts.append(f"### {chunk_info}")

                clean_content = PromptGenerator._clean_code_content(chunk.page_content)
                content_parts.append(f"```abap\n{clean_content}\n```")

        return "\n\n".join(content_parts)

    @staticmethod
    def _clean_code_content(content: str) -> str:
        """Remove context prefix from code content if present."""
        if content.startswith("[DOCUMENT_CONTEXT]"):
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if line.strip() == "[/DOCUMENT_CONTEXT]":
                    return "\n".join(lines[i + 2 :])  # Skip context section and empty line
        return content


# Enhanced integration class for webapp usage with ChatOllama support
class EnhancedPromptIntegration:
    """Enhanced integration for webapp usage with ChatOllama and gemma3:4b support."""

    @staticmethod
    def generate_ollama_prompt(
        abap_documents: List[Document],
        markdown_documents: List[Document],
        template_type: str = "abap_technical_specification",
        model_name: str = "gemma3:4b",
    ) -> str:
        """
        Generate a prompt optimized for ChatOllama with gemma3:4b model.

        Args:
            abap_documents: List of ABAP code document chunks
            markdown_documents: List of markdown specification template chunks
            template_type: Type of template being used
            model_name: Ollama model name (default: gemma3:4b)

        Returns:
            Formatted prompt string optimized for ChatOllama
        """

        additional_context = f"""
        Model Configuration:
        - Target Model: {model_name}
        - Framework: ChatOllama (LangChain)
        - Expected Output: Structured technical specification document
        - Format: Markdown with ABAP code examples
        """

        additional_instructions = """
        Generate a well-structured, comprehensive technical specification that:
        1. Follows the provided template structure
        2. Maps ABAP code elements to appropriate sections
        3. Uses clear markdown formatting
        4. Includes relevant code snippets
        5. Provides actionable technical details
        """

        return PromptGenerator.generate_enhanced_prompt(
            abap_documents=abap_documents,
            markdown_documents=markdown_documents,
            template_type=template_type,
            additional_context=additional_context,
            additional_instructions=additional_instructions,
        )

    @staticmethod
    def generate_prompt_by_document_ids(
        abap_documents: List[Document],
        markdown_documents: List[Document],
        abap_doc_id: Optional[str] = None,
        template_doc_id: Optional[str] = None,
        template_type: str = "abap_technical_specification",
    ) -> str:
        """
        Generate prompt for specific document IDs.

        Args:
            abap_documents: All available ABAP document chunks
            markdown_documents: All available markdown document chunks
            abap_doc_id: Specific ABAP document ID to process (None for all)
            template_doc_id: Specific template document ID to use (None for all)
            template_type: Type of template being used

        Returns:
            Formatted prompt string
        """
        from dcoument_splitter import DocumentSplitter

        # Filter ABAP documents if specific ID requested
        if abap_doc_id:
            filtered_abap = DocumentSplitter.get_chunks_by_document(abap_documents, abap_doc_id)
            if not filtered_abap:
                raise ValueError(f"No ABAP chunks found for document: {abap_doc_id}")
        else:
            filtered_abap = abap_documents

        # Filter template documents if specific ID requested
        if template_doc_id:
            filtered_templates = DocumentSplitter.get_chunks_by_document(markdown_documents, template_doc_id)
            if not filtered_templates:
                raise ValueError(f"No template chunks found for document: {template_doc_id}")
        else:
            filtered_templates = markdown_documents

        return EnhancedPromptIntegration.generate_ollama_prompt(
            abap_documents=filtered_abap, markdown_documents=filtered_templates, template_type=template_type
        )

    @staticmethod
    def prepare_for_chat_ollama(
        abap_documents: List[Document],
        markdown_documents: List[Document],
        system_message: str = "You are an expert ABAP developer and technical documentation specialist.",
        template_type: str = "abap_technical_specification",
    ) -> Dict[str, str]:
        """
        Prepare prompt and system message for ChatOllama usage.

        Args:
            abap_documents: List of ABAP code document chunks
            markdown_documents: List of markdown specification template chunks
            system_message: System message for ChatOllama
            template_type: Type of template being used

        Returns:
            Dictionary with 'system' and 'human' messages for ChatOllama
        """

        human_prompt = EnhancedPromptIntegration.generate_ollama_prompt(
            abap_documents=abap_documents, markdown_documents=markdown_documents, template_type=template_type
        )

        return {"system": system_message, "human": human_prompt}


# Backward compatibility aliases
PromptIntegration = EnhancedPromptIntegration  # For existing code compatibility
