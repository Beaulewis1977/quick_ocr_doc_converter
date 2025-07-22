class OcrDocumentConverter < Formula
  desc "Enterprise-grade OCR and document conversion tool"
  homepage "https://github.com/Beaulewis1977/quick_ocr_doc_converter"
  url "https://github.com/Beaulewis1977/quick_ocr_doc_converter/archive/v3.1.0.tar.gz"
  sha256 "GET_SHA256_AFTER_RELEASE"
  license "MIT"

  depends_on "python@3.11"
  depends_on "tesseract"
  depends_on "tesseract-lang"

  def install
    # Create virtual environment
    venv = virtualenv_create(libexec, "python3.11")
    
    # Install Python dependencies
    venv.pip_install_and_link buildpath
    
    # Create wrapper scripts
    (bin/"ocr-convert").write <<~EOS
      #!/bin/bash
      exec "#{libexec}/bin/python" "#{libexec}/bin/ocr-convert" "$@"
    EOS
    
    (bin/"doc-convert").write <<~EOS
      #!/bin/bash
      exec "#{libexec}/bin/python" "#{libexec}/bin/doc-convert" "$@"
    EOS
    
    (bin/"ocr-document-converter").write <<~EOS
      #!/bin/bash
      exec "#{libexec}/bin/python" "#{libexec}/bin/ocr-document-converter" "$@"
    EOS
    
    # Make scripts executable
    chmod 0755, bin/"ocr-convert"
    chmod 0755, bin/"doc-convert"
    chmod 0755, bin/"ocr-document-converter"
  end

  test do
    # Test CLI version
    assert_match "OCR Document Converter 3.1.0", shell_output("#{bin}/ocr-convert --version")
    assert_match "Quick Document Convertor 3.1.0", shell_output("#{bin}/doc-convert --version")
    
    # Test basic functionality
    (testpath/"test.txt").write("Hello World")
    system bin/"doc-convert", "test.txt", "-o", "test.md", "-t", "md"
    assert_predicate testpath/"test.md", :exist?
  end
end