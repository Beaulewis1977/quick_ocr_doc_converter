# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup and documentation

## [3.1.0] - 2024-12-22

### Added
- **Complete GUI Integration**: All features now unified in single main GUI interface
- **Google Vision API Support**: Full cloud OCR integration with service account authentication
- **Dual OCR Engine System**: Choice between free (Tesseract/EasyOCR) and API-based OCR
- **Secure Configuration Manager**: Encrypted storage for API keys and sensitive settings
- **Advanced OCR Settings GUI**: Tabbed interface for backends, processing, and security
- **Bidirectional Markdown Editor**: Live preview and real-time editing capabilities
- **Thread Control System**: Adjustable processing threads with quality settings
- **VB6/VFP9 Integration Package**: Complete legacy application support with examples
- **Legacy Integration GUI Tab**: Integrated VB6/VFP9 code generation and DLL builder in main interface
- **Enhanced Windows Installer**: Improved PyInstaller build with proper dependencies
- **Unified Launcher System**: Consolidated to main GUI and VB6/VFP9 tools only

### Enhanced
- **Main GUI Interface**: Tabbed design with all tools, settings, and functions integrated (now includes Legacy Integration tab)
- **OCR Processing**: Support for multiple backends with seamless switching
- **Document Reader**: Enhanced file type support and preview capabilities
- **Cross-Platform Support**: Updated installers for Windows, macOS, and Linux
- **Version Consistency**: All references updated to v3.1.0 across entire codebase

### Fixed
- **PyInstaller Path Errors**: Resolved file existence evaluation issues
- **Google Vision Implementation**: Added missing backend that was listed but not implemented
- **Import Dependencies**: Made encryption optional with graceful fallback
- **GUI Navigation**: Unified interface eliminates separate dialogs and windows
- **Installer Consistency**: All platforms now reference correct main application file

### Technical Improvements
- **Security**: Optional encryption for sensitive configuration data
- **Performance**: Multi-threaded processing with user-configurable thread counts
- **Reliability**: Comprehensive error handling and user feedback systems
- **Maintainability**: Consolidated codebase with clear separation of concerns

## [2.0.0] - 2024-12-11

### Added
- Universal document converter with GUI interface
- Support for 5 input formats: DOCX, PDF, TXT, HTML, RTF
- Support for 4 output formats: Markdown, TXT, HTML, RTF
- Drag-and-drop functionality for files and folders
- Batch processing with recursive folder support
- Real-time progress tracking and detailed results
- Auto-detection of input file formats
- Modern tkinter-based GUI with intuitive workflow
- Comprehensive error handling and user feedback
- Cross-platform compatibility (Windows, macOS, Linux)
- Offline operation with no external API dependencies
- Configurable options for folder structure preservation
- File overwrite protection with user confirmation

### Technical Features
- Modular architecture with separated readers and writers
- Format-specific processing classes for each supported type
- Threading for non-blocking UI during conversions
- Comprehensive test suite with format compatibility testing
- Performance optimizations for speed and memory usage
- Unicode encoding detection and handling
- Robust file I/O with proper error recovery

### Documentation
- Complete README with installation and usage instructions
- Product Requirements Document (PRD)
- Development guidelines (augment_rules.md)
- Comprehensive inline code documentation
- Performance benchmarks and system requirements
- Troubleshooting guide and FAQ section

### Dependencies
- python-docx: Microsoft Word document processing
- PyPDF2: PDF text extraction
- beautifulsoup4: HTML parsing and processing
- striprtf: Rich Text Format processing
- tkinterdnd2: Enhanced drag-and-drop support

### Performance
- Conversion times under 1 second for typical documents
- Memory usage optimized for large file processing
- Efficient batch processing for multiple files
- Responsive GUI during long operations

### Security
- All processing happens locally on user's machine
- No network communication or external API calls
- Secure temporary file handling and cleanup
- Input validation and sanitization

## [1.0.0] - 2024-11-01

### Added
- Basic document conversion functionality
- Simple GUI interface
- Support for DOCX, PDF, TXT to Markdown conversion
- Basic batch processing
- Initial project structure and documentation

---

## Release Notes

### Version 2.0.0 - Universal Format Support
This major release transforms the application into a comprehensive document conversion tool with support for multiple input and output formats, enhanced GUI, and professional-grade features.

**Key Highlights:**
- **5x4 Format Matrix**: Convert between 20 different format combinations
- **Modern Interface**: Complete GUI redesign with drag-and-drop support
- **Batch Processing**: Handle entire folders with recursive processing
- **Real-time Feedback**: Progress tracking and detailed conversion results
- **Zero Dependencies**: Works completely offline without external services

**Breaking Changes:**
- Updated GUI layout and workflow
- New command-line interface for programmatic usage
- Enhanced error handling may change error message formats

**Migration Guide:**
- No migration needed for existing users
- New features are additive and backward compatible
- Previous conversion results remain valid

**Known Issues:**
- PDF conversion limited to text extraction (no images)
- Complex HTML layouts may lose some formatting
- Very large files (>100MB) may require additional processing time

**System Requirements:**
- Python 3.7 or higher
- 50MB available disk space
- 100MB RAM for typical operations
- Cross-platform: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)

---

## Contributing

When contributing to this project, please:
1. Update the CHANGELOG.md with details of changes
2. Follow the format: Added/Changed/Deprecated/Removed/Fixed/Security
3. Include version numbers and dates
4. Reference issue numbers where applicable
5. Keep descriptions clear and user-focused

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for backward-compatible functionality additions  
- **PATCH** version for backward-compatible bug fixes

## Release Process

1. Update version numbers in relevant files
2. Update CHANGELOG.md with new version section
3. Create git tag with version number
4. Push changes and tag to repository
5. Create GitHub release with release notes
6. Update documentation if needed
