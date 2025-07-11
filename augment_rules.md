# Augment Rules for Quick Document Converter

## Project Overview
This is a Python-based universal document converter application with a modern GUI interface. The application converts between multiple document formats (DOCX, PDF, TXT, HTML, RTF) with drag-and-drop functionality and batch processing capabilities.

## Code Style and Standards

### Python Code Style
- Follow PEP 8 Python style guidelines
- Use type hints for all function parameters and return values
- Include comprehensive docstrings for all classes and methods
- Use descriptive variable and function names
- Maintain consistent indentation (4 spaces)
- Keep line length under 88 characters (Black formatter standard)

### File Organization
- Main application logic in `universal_document_converter.py`
- GUI components should be modular and well-separated
- Utility functions in separate modules when appropriate
- Test files should mirror the structure of source files

### Documentation Standards
- All public methods must have docstrings
- Include examples in docstrings for complex functions
- Document any external dependencies and their purposes
- Maintain up-to-date README with installation and usage instructions

## Development Guidelines

### Dependencies Management
- Use `requirements.txt` for dependency management
- Pin specific versions for production dependencies
- Document the purpose of each dependency
- Prefer lightweight libraries when possible
- Avoid unnecessary external API dependencies (keep it offline-capable)

### Error Handling
- Implement comprehensive error handling for file operations
- Provide user-friendly error messages in the GUI
- Log errors appropriately for debugging
- Handle encoding issues gracefully for text files
- Validate file formats before processing

### Testing Requirements
- Maintain comprehensive test coverage
- Test all supported file format conversions
- Include edge cases and error conditions
- Test GUI functionality where possible
- Performance testing for large files and batch operations

### GUI Development
- Use tkinter for cross-platform compatibility
- Implement drag-and-drop functionality
- Provide real-time progress feedback
- Ensure responsive UI during long operations
- Follow modern UI/UX principles

## Security Considerations

### File Handling
- Validate file types before processing
- Sanitize file paths to prevent directory traversal
- Handle large files without memory exhaustion
- Implement proper temporary file cleanup
- Validate file permissions before writing

### Data Privacy
- All processing must happen locally (no external API calls)
- No data should be transmitted over the network
- Temporary files should be securely cleaned up
- User file paths should not be logged or stored

## Performance Guidelines

### Optimization Targets
- File conversion should complete in under 1 second for typical documents
- Memory usage should remain reasonable for large files
- GUI should remain responsive during processing
- Batch operations should be efficient and provide progress feedback

### Resource Management
- Use generators for processing large files
- Implement proper memory cleanup
- Avoid loading entire files into memory when possible
- Use threading for non-blocking GUI operations

## Architecture Principles

### Modularity
- Separate concerns between file reading, processing, and writing
- Use factory patterns for format-specific handlers
- Keep GUI logic separate from conversion logic
- Make the system extensible for new formats

### Reliability
- Graceful degradation when optional features fail
- Robust error recovery
- Consistent behavior across different platforms
- Proper resource cleanup in all code paths

## Contribution Guidelines

### Code Review Requirements
- All changes must include appropriate tests
- Documentation must be updated for API changes
- Performance impact should be considered
- Security implications must be reviewed

### Feature Development
- New file formats should follow existing patterns
- GUI changes should maintain consistency
- New features should include comprehensive documentation
- Consider backward compatibility

## Deployment and Distribution

### Packaging
- Ensure all dependencies are properly specified
- Test on multiple Python versions (3.7+)
- Verify cross-platform compatibility
- Include proper license information

### Release Process
- Update version numbers consistently
- Maintain changelog for user-facing changes
- Test installation process on clean environments
- Verify all features work in packaged version

## Maintenance Guidelines

### Code Quality
- Regular dependency updates with testing
- Periodic code review for improvements
- Performance monitoring and optimization
- Security vulnerability scanning

### User Support
- Maintain clear troubleshooting documentation
- Provide helpful error messages
- Include usage examples and tutorials
- Respond to user feedback and issues

## Technology Stack Constraints

### Core Technologies
- Python 3.7+ (maintain backward compatibility)
- tkinter for GUI (built-in, cross-platform)
- Standard library preferred when possible
- Minimal external dependencies

### Approved Libraries
- `python-docx` for Word document processing
- `PyPDF2` for PDF text extraction
- `beautifulsoup4` for HTML parsing
- `striprtf` for RTF processing
- `tkinterdnd2` for enhanced drag-and-drop

### Prohibited Dependencies
- No web frameworks or server components
- No external API clients
- No heavy ML/AI libraries
- No platform-specific dependencies
