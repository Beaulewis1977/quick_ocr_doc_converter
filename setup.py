#!/usr/bin/env python3
"""
Setup script for OCR Document Converter
For publishing to PyPI
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="ocr-document-converter",
    version="3.1.0",
    author="Beau Lewis",
    author_email="blewisxx@gmail.com",
    description="Enterprise-grade OCR and document conversion tool with dual OCR engines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Beaulewis1977/quick_ocr_doc_converter",
    project_urls={
        "Bug Tracker": "https://github.com/Beaulewis1977/quick_ocr_doc_converter/issues",
        "Documentation": "https://github.com/Beaulewis1977/quick_ocr_doc_converter/blob/main/OCR_README.md",
        "Source Code": "https://github.com/Beaulewis1977/quick_ocr_doc_converter",
    },
    packages=find_packages(exclude=["tests*", "dev_docs_backup*", "build_installer*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: General",
        "Topic :: Multimedia :: Graphics :: Capture :: Digital Camera",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
    ],
    keywords="ocr, document conversion, pdf, tesseract, easyocr, text extraction",
    python_requires=">=3.8",
    install_requires=[
        "Pillow>=9.0.0",
        "PyPDF2>=3.0.0",
        "python-docx>=0.8.11",
        "beautifulsoup4>=4.11.0",
        "striprtf>=0.0.22",
        "ebooklib>=0.18",
        "pytesseract>=0.3.10",
        "opencv-python>=4.7.0",
        "numpy>=1.21.0",
    ],
    extras_require={
        "easyocr": ["easyocr>=1.6.2"],
        "cloud": [
            "google-cloud-vision>=3.0.0",
            "boto3>=1.26.0",
            "azure-cognitiveservices-vision-computervision>=0.9.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "bandit>=1.7.0",
            "safety>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ocr-convert=cli_ocr:main",
            "doc-convert=cli:main",
        ],
        "gui_scripts": [
            "ocr-document-converter=universal_document_converter_ocr:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ocr_engine": ["*.json"],
    },
    zip_safe=False,
)