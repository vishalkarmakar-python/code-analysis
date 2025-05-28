# 1. Enhanced prompt_ts.py with optimization features
from langchain_core.documents.base import Document
from typing import ClassVar, List, Self, Dict, Any
import json


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
                "Dependencies"
            ]

    def get_prompt_technical_specification(
        self, 
        code: List[Document], 
        spec: List[Document],
        mode: str = "comprehensive"  # Options: "core", "comprehensive", "segmented"
    ) -> str:
        """
        Generate optimized prompt based on selected mode
        
        Args:
            code: List of code documents
            spec: List of specification template documents
            mode: Processing mode - "core", "comprehensive", "segmented"
        """
        code_content = self._extract_and_optimize_code(code)
        
        if mode == "core":
            return self._get_core_prompt(code_content, spec)
        elif mode == "segmented":
            return self._get_segmented_prompt(code_content, spec)
        else:
            return self._get_comprehensive_prompt(code_content, spec)

    def _get_core_prompt(self, code_content: str, spec: List[Document]) -> str:
        """Generate focused prompt for core sections only"""
        core_template = self._extract_core_template_sections(spec)
        
        return f"""
CONTEXT: You are an experienced SAP ABAP technical consultant with 10 years of experience creating comprehensive technical documentation.

TASK: Analyze the provided ABAP code and generate technical specifications focusing on the most critical aspects.

INSTRUCTIONS:
1. Prioritize accuracy over completeness
2. Focus on core business logic and object relationships
3. Use clear, professional technical language
4. Structure output according to the template provided

CODE TO ANALYZE:
{code_content}

FOCUS AREAS (Priority Order):
1. Object Structure and Relationships
2. Key Business Logic and Methods  
3. Database Design and CDS Views (if applicable)
4. Dependencies and Integration Points

TEMPLATE SECTIONS TO FOLLOW:
{core_template}

OUTPUT REQUIREMENTS:
- Start with Document Information and Overview
- Focus on sections 1-7 from the template
- Provide detailed analysis of business logic
- Include dependency information
- Use professional technical writing style

CONSTRAINTS:
- Maximum response length: Focus on essential information
- Use bullet points for complex lists
- Include code snippets only when necessary for understanding
- Ensure all technical terms are properly explained
"""

    def _get_comprehensive_prompt(self, code_content: str, spec: List[Document]) -> str:
        """Generate full comprehensive prompt"""
        spec_content = self._extract_spec_from_documents(spec)
        
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

    def _get_segmented_prompt(self, code_content: str, spec: List[Document]) -> str:
        """Generate prompt for segmented processing"""
        return f"""
CONTEXT: You are an SAP ABAP technical documentation specialist.

SEGMENTED ANALYSIS REQUEST: This is part of a larger technical specification. Focus on analyzing the provided code sections systematically.

CODE TO ANALYZE:
{code_content}

ANALYSIS APPROACH:
1. Code Structure Analysis
   - Identify main components (classes, views, services)
   - Map relationships between objects
   - Document inheritance and interfaces

2. Business Logic Documentation
   - Extract key methods and their purposes
   - Identify validation rules and business checks
   - Document workflow and processing flow

3. Technical Implementation Details
   - Database table relationships
   - CDS view structure and annotations
   - RAP behavior patterns

OUTPUT FORMAT:
Please provide analysis in structured sections that can be easily integrated into a larger technical specification document.

FOCUS: Provide detailed technical analysis that will serve as building blocks for complete documentation.
"""

    def _extract_and_optimize_code(self, documents: List[Document]) -> str:
        """Extract and optimize code content with length management"""
        code_sections: List[str] = []
        total_length = 0
        
        for i, code in enumerate(documents):
            if hasattr(code, "page_content") and code.page_content:
                content: str = code.page_content.strip()
                if content:
                    # Check if adding this section would exceed limit
                    section_content = f"--- Code Section {i + 1} ---\n{content}\n"
                    
                    if total_length + len(section_content) > self._max_code_length:
                        # Truncate or summarize this section
                        truncated_content = self._truncate_code_section(content, 
                                                                      self._max_code_length - total_length)
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
        lines = content.split('\n')
        important_lines = []
        current_length = 0
        
        for line in lines:
            # Prioritize lines with key ABAP keywords
            if any(keyword in line.upper() for keyword in 
                   ['CLASS', 'METHOD', 'DEFINE', 'SELECT', 'TYPES', 'DATA']):
                if current_length + len(line) < max_length:
                    important_lines.append(line)
                    current_length += len(line) + 1
            elif current_length + len(line) < max_length * 0.8:  # Fill remaining with other lines
                important_lines.append(line)
                current_length += len(line) + 1
        
        result = '\n'.join(important_lines)
        if len(result) < len(content):
            result += f"\n\n... [Content truncated. Original length: {len(content)} chars]"
        
        return result

    def _extract_core_template_sections(self, documents: List[Document]) -> str:
        """Extract only core sections from template"""
        spec_content = self._extract_spec_from_documents(documents)
        
        # Extract only priority sections (simplified for core mode)
        core_sections = [
            "## 1. Document Information",
            "## 2. Overview", 
            "## 3. Object Structure",
            "## 5. Method/Function Specifications",
            "## 7. Business Logic",
            "## 14. Dependencies"
        ]
        
        # This is a simplified extraction - in practice, you might want to 
        # parse the markdown more sophisticated
        return f"""
Focus on these key sections from the template:

1. Document Information - Basic metadata and identification
2. Overview - Purpose, business context, scope, functional requirements  
3. Object Structure - Class/object definitions, design patterns
4. Method/Function Specifications - Key methods and their purposes
5. Business Logic - Rules, validations, processing flow
6. Dependencies - System and object dependencies

Use the full template structure but prioritize these sections with detailed analysis.
Template reference: {spec_content[:2000]}...
"""

    def _extract_code_from_documents(self, documents: List[Document]) -> str:
        """Original method maintained for backward compatibility"""
        return self._extract_and_optimize_code(documents)

    def _extract_spec_from_documents(self, documents: List[Document]) -> str:
        """Extract specification template content"""
        spec_sections: List[str] = []
        for i, spec in enumerate(documents):
            if hasattr(spec, "page_content") and spec.page_content:
                content: str = spec.page_content.strip()
                if content:
                    spec_sections.append(f"--- Template Section {i + 1} ---\n{content}\n")

        return "\n".join(spec_sections)

    def get_processing_statistics(self, code: List[Document]) -> Dict[str, Any]:
        """Get statistics about the code to be processed"""
        total_chars = sum(len(doc.page_content) for doc in code if hasattr(doc, 'page_content'))
        return {
            "total_documents": len(code),
            "total_characters": total_chars,
            "estimated_tokens": total_chars // 4,  # Rough estimate
            "recommended_mode": self._recommend_processing_mode(total_chars),
            "fits_in_context": total_chars < self._max_code_length
        }

    def _recommend_processing_mode(self, total_chars: int) -> str:
        """Recommend processing mode based on content size"""
        if total_chars < 8000:
            return "comprehensive"
        elif total_chars < 20000:
            return "core"
        else:
            return "segmented"


# 2. Enhanced webapp.py with mode selection
# Add this to your webapp.py file in the appropriate section:

def add_processing_mode_selection():
    """Add processing mode selection to Streamlit interface"""
    st.subheader("Processing Configuration")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        processing_mode = st.selectbox(
            "Processing Mode",
            options=["comprehensive", "core", "segmented"],
            help="""
            - Comprehensive: Full detailed analysis (recommended for smaller files)
            - Core: Focus on essential sections (recommended for medium files)  
            - Segmented: Simplified analysis (recommended for large files)
            """
        )
    
    with col2:
        if st.button("Analyze Code Size", help="Get recommendations for processing mode"):
            if code_files:  # Assuming code_files is available in scope
                # This would need to be integrated into your existing webapp.py logic
                prompt_loader = Prompt()
                # Load documents first
                text_document_loader = TextDocumentLoader()
                documents = text_document_loader.load_text_documents(file_list=file_info_list)
                
                stats = prompt_loader.get_processing_statistics(documents)
                
                st.info(f"""
                **Analysis Results:**
                - Total Documents: {stats['total_documents']}
                - Total Characters: {stats['total_characters']:,}
                - Estimated Tokens: {stats['estimated_tokens']:,}
                - Recommended Mode: **{stats['recommended_mode']}**
                - Fits in Context: {'✅ Yes' if stats['fits_in_context'] else '❌ No'}
                """)
    
    return processing_mode

# 3. Updated section in webapp.py for using the new prompt system
def generate_documentation_with_mode(processing_mode: str):
    """Updated documentation generation with mode selection"""
    
    # Your existing code for loading documents...
    text_document_loader: TextDocumentLoader = TextDocumentLoader()
    documents: List[Document] = text_document_loader.load_text_documents(file_list=file_info_list)

    markdown_document_loader: MarkdownDocumentLoader = MarkdownDocumentLoader()
    markdown_file_list: List[Any] = []
    markdown_file_list.append({
        "file_name": "TS.md",
        "file_path": path.join(getcwd(), "document_generator", "app", "templates", "TS.md"),
    })
    md_document: List[Document] = markdown_document_loader.load_markdown_documents(file_list=markdown_file_list)
    
    # Initialize the prompt with mode selection
    prompt_loader: Prompt = Prompt()
    
    # Get statistics for user information
    stats = prompt_loader.get_processing_statistics(documents)
    st.info(f"Processing {stats['total_documents']} documents with {stats['estimated_tokens']:,} estimated tokens using **{processing_mode}** mode")
    
    # Generate prompt with selected mode
    prompt: str = prompt_loader.get_prompt_technical_specification(
        code=documents,
        spec=md_document,
        mode=processing_mode
    )
    
    if documents:
        ollama: Llama3 = Llama3()
        if ollama.initialize_llm(model_name="OLLAMA"):
            st.success("Connected to Ollama server successfully.")
            
            # Show progress indicator for longer processing
            with st.spinner(f"Generating documentation in {processing_mode} mode..."):
                with ollama.get_llm() as model:
                    result: BaseMessage = model.invoke(input=prompt)
                    
            # Display results
            st.success(f"Documentation generated successfully in {processing_mode} mode!")
            
            # Show the generated content
            if hasattr(result, 'content') and result.content:
                st.subheader("Generated Documentation")
                st.markdown(result.content)
                
                # Add download button for the generated documentation
                st.download_button(
                    label=f"Download Documentation ({output_format})",
                    data=result.content,
                    file_name=f"technical_specification_{processing_mode}.md",
                    mime="text/markdown"
                )

# 4. Environment configuration example (.env file)
OLLAMA_MODEL=llama3.1:8b
OLLAMA_MODEL_BASE_URL=http://localhost:11434
OLLAMA_MODEL_TEMPERATURE=0.3

# 5. Additional utility functions for the Prompt class
def get_segmented_prompts(self, code: List[Document], spec: List[Document], segment_size: int = 5000) -> List[str]:
    """Generate multiple prompts for segmented processing"""
    code_content = self._extract_code_from_documents(code)
    spec_content = self._extract_spec_from_documents(spec)
    
    # Split code into segments
    segments = self._split_content_into_segments(code_content, segment_size)
    prompts = []
    
    for i, segment in enumerate(segments):
        prompt: str = f"""
                        CONTEXT: You are an SAP ABAP technical documentation specialist.

                        SEGMENTED ANALYSIS - Part {i+1} of {len(segments)}

                        CODE SEGMENT TO ANALYZE:
                        {segment}

                        TASK: Analyze this code segment and provide detailed technical documentation focusing on:
                        1. Object identification and structure
                        2. Method analysis and business logic
                        3. Database relationships (if applicable)
                        4. Integration points

                        OUTPUT: Provide structured analysis that can be integrated into a comprehensive technical specification.

                        This is segment {i+1} of {len(segments)}. Focus on this segment while maintaining consistency with overall application structure.
                       """
        prompts.append(prompt)
    
    return prompts

def _split_content_into_segments(self, content: str, segment_size: int) -> List[str]:
    """Split content into manageable segments"""
    if len(content) <= segment_size:
        return [content]
    
    segments = []
    lines = content.split('\n')
    current_segment = []
    current_size = 0
    
    for line in lines:
        if current_size + len(line) > segment_size and current_segment:
            segments.append('\n'.join(current_segment))
            current_segment = [line]
            current_size = len(line)
        else:
            current_segment.append(line)
            current_size += len(line) + 1
    
    if current_segment:
        segments.append('\n'.join(current_segment))
    
    return segments