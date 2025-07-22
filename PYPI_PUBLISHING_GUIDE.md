# PyPI Publishing Guide for OCR Document Converter

## 🚀 First-Time Setup

### 1. Create PyPI Account
1. Go to https://pypi.org/account/register/
2. Create your account
3. Verify your email

### 2. Generate API Token
1. Go to https://pypi.org/manage/account/
2. Scroll to "API tokens"
3. Click "Add API token"
4. Name: `ocr-document-converter`
5. Scope: "Entire account" (for first upload)
6. **Save the token immediately** (shown only once!)

### 3. Configure Token Locally
Create `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi

[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

Or use environment variable:
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE
```

## 📦 Publishing Process

### 1. Prepare the Package
```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Install build tools
pip install --upgrade build twine

# Build the package
python -m build
```

This creates:
- `dist/ocr-document-converter-3.1.0.tar.gz` (source distribution)
- `dist/ocr_document_converter-3.1.0-py3-none-any.whl` (wheel)

### 2. Test the Package
```bash
# Check package
twine check dist/*

# Test installation in a virtual environment
python -m venv test_install
source test_install/bin/activate  # Windows: test_install\Scripts\activate
pip install dist/ocr_document_converter-3.1.0-py3-none-any.whl

# Test the installed package
ocr-convert --version
doc-convert --version
ocr-document-converter  # Should launch GUI
```

### 3. Upload to Test PyPI (Optional but Recommended)
```bash
# Upload to test repository
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ ocr-document-converter
```

### 4. Upload to PyPI
```bash
# Upload to PyPI
twine upload dist/*

# You'll see:
# Uploading distributions to https://upload.pypi.org/legacy/
# Uploading ocr_document_converter-3.1.0-py3-none-any.whl
# Uploading ocr-document-converter-3.1.0.tar.gz
# View at: https://pypi.org/project/ocr-document-converter/3.1.0/
```

## ✅ Post-Publishing Verification

### 1. Test Installation
```bash
# In a new environment
pip install ocr-document-converter

# Verify console scripts
ocr-convert --help
doc-convert --help

# Verify GUI script
ocr-document-converter
```

### 2. Check PyPI Page
Visit: https://pypi.org/project/ocr-document-converter/
- Verify description renders correctly
- Check all links work
- Confirm version number

### 3. Test Different Platforms
```bash
# Windows
pip install ocr-document-converter
ocr-convert test.pdf -o test.txt --ocr

# macOS/Linux
pip3 install ocr-document-converter
ocr-convert test.pdf -o test.txt --ocr
```

## 🔧 Troubleshooting

### Common Issues

1. **"Invalid distribution file"**
   - Run `twine check dist/*` first
   - Ensure no spaces in filenames
   - Check MANIFEST.in is correct

2. **"Package name already exists"**
   - Package names are unique on PyPI
   - Cannot delete/reuse names
   - Use different name if needed

3. **"Invalid token"**
   - Tokens are shown only once
   - Generate new token if lost
   - Check token starts with `pypi-`

4. **Missing files in package**
   - Check MANIFEST.in
   - Verify package_data in setup.py
   - Use `tar -tf dist/*.tar.gz` to inspect

## 📝 Updating the Package

For future updates:
```bash
# 1. Update version in:
#    - setup.py
#    - pyproject.toml
#    - __init__.py files

# 2. Build and upload
rm -rf dist/ build/
python -m build
twine upload dist/*
```

## 🎯 Package URLs

Once published:
- PyPI page: https://pypi.org/project/ocr-document-converter/
- Installation: `pip install ocr-document-converter`
- Documentation: Links to GitHub README
- Statistics: https://pypistats.org/packages/ocr-document-converter

## 💡 Best Practices

1. **Always test locally first**
2. **Use TestPyPI for first-time publishers**
3. **Include comprehensive README**
4. **Tag releases in git**
5. **Update changelog for each version**