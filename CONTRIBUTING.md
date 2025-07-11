# Contributing to Quick Document Converter

Thank you for your interest in contributing to Quick Document Converter! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title** describing the issue
- **Detailed description** of the problem
- **Steps to reproduce** the behavior
- **Expected vs actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Screenshots** if applicable
- **Error messages** or logs

### Suggesting Features

Feature suggestions are welcome! Please:

- Check existing issues and discussions first
- Provide a clear use case for the feature
- Explain how it would benefit users
- Consider implementation complexity
- Be open to discussion and feedback

### Pull Requests

1. **Fork** the repository
2. **Create a branch** for your feature/fix
3. **Make your changes** following our coding standards
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Submit a pull request** with a clear description

## 🛠️ Development Setup

### Prerequisites

- Python 3.7 or higher
- Git
- Text editor or IDE

### Local Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/quick_doc_convertor.git
cd quick_doc_convertor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_converter.py

# Run the application
python universal_document_converter.py
```

## 📝 Coding Standards

### Python Style Guide

- Follow **PEP 8** Python style guidelines
- Use **type hints** for function parameters and return values
- Write **comprehensive docstrings** for all classes and methods
- Use **descriptive variable names**
- Keep **line length under 88 characters**
- Use **4 spaces** for indentation

### Code Quality

```python
# Good example
def convert_document(input_path: str, output_format: str) -> bool:
    """
    Convert a document to the specified output format.
    
    Args:
        input_path: Path to the input document
        output_format: Target format (markdown, txt, html, rtf)
        
    Returns:
        True if conversion successful, False otherwise
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If output format is not supported
    """
    # Implementation here
    pass
```

### Documentation

- **All public methods** must have docstrings
- Include **examples** in docstrings for complex functions
- Update **README.md** for user-facing changes
- Update **CHANGELOG.md** for all changes
- Comment **complex logic** inline

## 🧪 Testing Guidelines

### Test Requirements

- **All new features** must include tests
- **Bug fixes** should include regression tests
- **Maintain test coverage** above 80%
- **Test edge cases** and error conditions

### Running Tests

```bash
# Run all tests
python test_converter.py

# Run specific test categories
python -m pytest tests/ -v

# Check test coverage
python -m coverage run test_converter.py
python -m coverage report
```

### Test Structure

```python
def test_docx_to_markdown_conversion():
    """Test DOCX to Markdown conversion functionality."""
    # Arrange
    converter = UniversalConverter()
    input_file = "test_files/sample.docx"
    
    # Act
    result = converter.convert_file(input_file, "output.md", "docx", "markdown")
    
    # Assert
    assert result is True
    assert os.path.exists("output.md")
    # Additional assertions...
```

## 🏗️ Architecture Guidelines

### Adding New File Formats

1. **Create reader class** inheriting from `DocumentReader`
2. **Create writer class** inheriting from `DocumentWriter`
3. **Update format detection** in `FormatDetector`
4. **Add comprehensive tests**
5. **Update documentation**

### Code Organization

```
quick_doc_convertor/
├── universal_document_converter.py  # Main application
├── readers/                         # Format-specific readers
├── writers/                         # Format-specific writers
├── tests/                          # Test files
├── docs/                           # Documentation
└── examples/                       # Usage examples
```

## 🔄 Git Workflow

### Branch Naming

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Examples:
- `feat(converter): add EPUB format support`
- `fix(gui): resolve drag-drop issue on macOS`
- `docs(readme): update installation instructions`

### Pull Request Process

1. **Update documentation** for any user-facing changes
2. **Add tests** for new functionality
3. **Update CHANGELOG.md** with your changes
4. **Ensure all tests pass**
5. **Request review** from maintainers

## 📋 Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `question` - Further information requested

## 🎯 Priority Areas

We especially welcome contributions in these areas:

### High Priority
- **Performance optimizations** for large files
- **Additional file format support** (EPUB, ODT, etc.)
- **Improved error handling** and user feedback
- **Cross-platform testing** and compatibility

### Medium Priority
- **GUI improvements** and modern styling
- **Command-line interface** enhancements
- **Batch processing** optimizations
- **Documentation** and tutorials

### Low Priority
- **Code refactoring** and cleanup
- **Test coverage** improvements
- **Development tooling** enhancements

## 🚀 Release Process

### For Maintainers

1. **Update version** in relevant files
2. **Update CHANGELOG.md** with release notes
3. **Create and push git tag**
4. **Create GitHub release**
5. **Update documentation** if needed

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible functionality
- **PATCH**: Backward-compatible bug fixes

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: [blewisxx@gmail.com](mailto:blewisxx@gmail.com) for direct contact

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- **README.md** contributors section
- **Release notes** for significant contributions
- **CHANGELOG.md** for all contributions

Thank you for helping make Quick Document Converter better! 🎉
