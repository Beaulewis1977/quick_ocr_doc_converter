# Google Vision API Setup Guide

## 🔑 Complete Setup Guide for Google Vision API Integration

This guide covers setting up Google Vision API for premium OCR capabilities in OCR Document Converter v3.1.0.

---

## 📋 **Table of Contents**

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Google Cloud Setup](#google-cloud-setup)
4. [Application Configuration](#application-configuration)
5. [Testing and Verification](#testing-and-verification)
6. [Cost Management](#cost-management)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 **Overview**

### What is Google Vision API?
Google Vision API provides **cloud-based OCR** with superior accuracy compared to free alternatives:

- **99%+ accuracy** on printed text
- **Superior handwriting recognition**
- **Multi-language support** (100+ languages)
- **Document structure preservation**
- **Table and form recognition**
- **Automatic fallback** to free OCR if API fails

### Pricing Summary
- **First 1,000 requests/month**: FREE
- **Additional requests**: $1.50 per 1,000 requests
- **No setup fees** or monthly minimums
- **Pay only for what you use**

---

## 📋 **Prerequisites**

### System Requirements
- **OCR Document Converter v3.1.0** installed
- **Internet connection** for API calls
- **Google account** (free to create)
- **Credit card** (for billing setup, free tier available)

### Before You Begin
1. ✅ Ensure OCR Document Converter is working with free OCR
2. ✅ Have your Google account credentials ready
3. ✅ Understand the pricing model
4. ✅ Plan your monthly usage estimate

---

## ☁️ **Google Cloud Setup**

### Step 1: Create Google Cloud Project

#### 1.1 Access Google Cloud Console
1. **Go to**: [Google Cloud Console](https://console.cloud.google.com/)
2. **Sign in** with your Google account
3. **Accept** terms of service if prompted

#### 1.2 Create New Project
1. **Click** "Select a project" dropdown (top bar)
2. **Click** "New Project"
3. **Enter** project details:
   - **Project name**: `OCR-Document-Converter`
   - **Organization**: (leave default)
   - **Location**: (leave default)
4. **Click** "Create"
5. **Wait** for project creation (30-60 seconds)

#### 1.3 Select Your Project
1. **Click** project dropdown again
2. **Select** your new `OCR-Document-Converter` project

### Step 2: Enable Vision API

#### 2.1 Navigate to APIs & Services
1. **Click** ☰ (hamburger menu) → **APIs & Services** → **Library**
2. **Search** for "Cloud Vision API"
3. **Click** on "Cloud Vision API" result
4. **Click** "Enable" button
5. **Wait** for API to be enabled (30-60 seconds)

#### 2.2 Verify API is Enabled
1. **Go to** APIs & Services → **Enabled APIs**
2. **Confirm** "Cloud Vision API" is listed

### Step 3: Set Up Billing (Required)

#### 3.1 Enable Billing Account
1. **Go to** ☰ → **Billing**
2. **Click** "Link a billing account"
3. **Create billing account** or select existing one
4. **Add** payment method (credit card)
5. **Link** billing account to your project

#### 3.2 Set Up Budget Alerts (Recommended)
1. **Go to** Billing → **Budgets & alerts**
2. **Click** "Create budget"
3. **Configure** budget:
   - **Name**: "OCR Monthly Budget"
   - **Amount**: $10 (or your preferred limit)
   - **Alert thresholds**: 50%, 90%, 100%
4. **Save** budget

### Step 4: Create Service Account

#### 4.1 Navigate to IAM & Admin
1. **Go to** ☰ → **IAM & Admin** → **Service Accounts**
2. **Click** "Create Service Account"

#### 4.2 Configure Service Account
1. **Service account details**:
   - **Name**: `ocr-converter-service`
   - **ID**: (auto-generated)
   - **Description**: `Service account for OCR Document Converter`
2. **Click** "Create and Continue"

#### 4.3 Grant Permissions
1. **Select role**: "Vision API User"
2. **Click** "Continue"
3. **Click** "Done"

#### 4.4 Create and Download Key
1. **Click** on your service account name
2. **Go to** "Keys" tab
3. **Click** "Add Key" → "Create new key"
4. **Select** "JSON" format
5. **Click** "Create"
6. **Save** the downloaded JSON file securely
   - **Recommended location**: `C:\OCR-Converter\google-vision-key.json`
   - **Keep secure**: This file contains your API credentials

---

## ⚙️ **Application Configuration**

### Method 1: GUI Configuration (Recommended)

#### 1.1 Open OCR Settings
1. **Launch** OCR Document Converter
2. **Click** "Settings" or "OCR Settings"
3. **Navigate** to "Google Vision API" tab

#### 1.2 Upload API Key
1. **Click** "Browse" or "Upload Key File"
2. **Select** your downloaded JSON key file
3. **Click** "Open"
4. **Verify** key is loaded (green checkmark)

#### 1.3 Test Connection
1. **Click** "Test Connection"
2. **Wait** for verification (5-10 seconds)
3. **Confirm** "✅ Connected" status
4. **Click** "Save Settings"

### Method 2: Manual Configuration

#### 2.1 Set Environment Variable
```bash
# Windows Command Prompt
set GOOGLE_APPLICATION_CREDENTIALS=C:\OCR-Converter\google-vision-key.json

# Windows PowerShell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\OCR-Converter\google-vision-key.json"

# Linux/macOS
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/google-vision-key.json"
```

#### 2.2 Create Configuration File
Create `google_vision_config.json`:
```json
{
    "engine": "google_vision",
    "enabled": true,
    "service_account_key": "C:\\OCR-Converter\\google-vision-key.json",
    "confidence_threshold": 0.8,
    "features": ["TEXT_DETECTION", "DOCUMENT_TEXT_DETECTION"],
    "language_hints": ["en"],
    "fallback_enabled": true,
    "fallback_engines": ["tesseract", "easyocr"],
    "max_requests_per_minute": 60,
    "encryption": {
        "enabled": true,
        "encrypt_api_keys": true
    }
}
```

### Method 3: Command Line Configuration

#### 3.1 Test API with CLI
```bash
# Test Google Vision API
python cli_ocr.py test_image.jpg -o output.txt --engine google_vision

# Test with fallback enabled
python cli_ocr.py test_image.jpg -o output.txt --engine google_vision --fallback
```

---

## 🧪 **Testing and Verification**

### Test 1: Basic Functionality

#### 1.1 Prepare Test File
1. **Create** or download a test image with text
2. **Save** as `test_image.jpg` in OCR Converter folder

#### 1.2 Test via GUI
1. **Open** OCR Document Converter
2. **Select** test image file
3. **Enable** OCR mode
4. **Select** "Google Vision API" as OCR engine
5. **Click** "Convert"
6. **Verify** text extraction quality

#### 1.3 Test via Command Line
```bash
# Basic test
python cli_ocr.py test_image.jpg -o test_output.txt --engine google_vision

# Check output
type test_output.txt
```

### Test 2: Fallback System

#### 2.1 Test Offline Fallback
1. **Disconnect** internet temporarily
2. **Run** OCR conversion
3. **Verify** automatic fallback to Tesseract/EasyOCR
4. **Check** status messages show fallback occurred

#### 2.2 Test API Failure Handling
```bash
# Test with invalid credentials
python cli_ocr.py test_image.jpg -o output.txt --engine google_vision --test-fallback
```

### Test 3: Performance Comparison

#### 3.1 Compare OCR Engines
Create comparison test:
```bash
# Test with Tesseract
python cli_ocr.py test_image.jpg -o tesseract_output.txt --engine tesseract

# Test with Google Vision
python cli_ocr.py test_image.jpg -o google_output.txt --engine google_vision

# Compare results
fc tesseract_output.txt google_output.txt
```

#### 3.2 Accuracy Metrics
Use the GUI's built-in comparison tool:
1. **Go to** OCR Settings → Testing tab
2. **Upload** test image
3. **Click** "Compare All Engines"
4. **Review** accuracy and speed metrics

---

## 💰 **Cost Management**

### Understanding Costs

#### Pricing Breakdown
- **Text Detection**: $1.50 per 1,000 requests
- **Document Text Detection**: $1.50 per 1,000 requests
- **Free tier**: First 1,000 requests/month
- **No charges** for failed requests

#### Usage Examples
| Monthly Volume | Cost |
|---------------|------|
| 500 requests | FREE |
| 1,000 requests | FREE |
| 2,000 requests | $1.50 |
| 5,000 requests | $6.00 |
| 10,000 requests | $13.50 |

### Cost Optimization Strategies

#### 1. Enable Smart Fallback
```json
{
    "cost_optimization": {
        "use_free_for_simple_text": true,
        "google_vision_for_complex": true,
        "confidence_threshold": 0.85
    }
}
```

#### 2. Batch Processing
- **Process multiple files** in single sessions
- **Use batch API calls** when available
- **Combine small images** when practical

#### 3. Set Usage Limits
Configure in `google_vision_config.json`:
```json
{
    "usage_limits": {
        "max_requests_per_day": 100,
        "max_requests_per_month": 2000,
        "auto_disable_at_limit": true
    }
}
```

#### 4. Monitor Usage
1. **Go to** Google Cloud Console → Billing → Reports
2. **Filter** by "Cloud Vision API"
3. **Set up** billing alerts
4. **Review** monthly usage reports

---

## 🔧 **Advanced Configuration**

### Custom OCR Parameters

#### High-Quality Settings
```json
{
    "google_vision": {
        "image_context": {
            "language_hints": ["en", "fr", "de"],
            "crop_hints_params": {
                "aspect_ratios": [1.0, 1.5, 2.0]
            }
        },
        "features": [
            {
                "type": "DOCUMENT_TEXT_DETECTION",
                "max_results": 1
            }
        ]
    }
}
```

#### Performance Optimization
```json
{
    "performance": {
        "concurrent_requests": 5,
        "request_timeout": 30,
        "retry_count": 3,
        "cache_results": true,
        "cache_duration_hours": 24
    }
}
```

### Integration with Legacy Systems

#### VB6 Integration
```vb
Public Function ConvertWithGoogleVision(inputFile As String, outputFile As String) As Boolean
    Dim cmd As String
    Dim result As Long
    
    ' Use Google Vision API
    cmd = "python cli_ocr.py """ & inputFile & """ -o """ & outputFile & """ --engine google_vision --fallback"
    
    result = Shell(cmd, vbHide)
    Sleep 3000  ' Allow time for cloud processing
    
    ConvertWithGoogleVision = (Dir(outputFile) <> "")
End Function
```

#### VFP9 Integration
```foxpro
FUNCTION ConvertWithCloudOCR(tcInputFile, tcOutputFile)
    LOCAL lcCommand, lnResult
    
    lcCommand = 'python cli_ocr.py "' + tcInputFile + '" -o "' + ;
                tcOutputFile + '" --engine google_vision --fallback'
    
    RUN /N7 (lcCommand) TO lnResult
    
    RETURN (lnResult = 0) AND FILE(tcOutputFile)
ENDFUNC
```

---

## 🔍 **Troubleshooting**

### Common Issues and Solutions

#### Issue 1: "Authentication failed"
**Symptoms**: API calls fail with authentication error
**Solutions**:
```bash
# Check environment variable
echo %GOOGLE_APPLICATION_CREDENTIALS%

# Verify file exists and is readable
dir "C:\OCR-Converter\google-vision-key.json"

# Test authentication
python -c "from google.cloud import vision; client = vision.ImageAnnotatorClient(); print('Authentication successful')"
```

#### Issue 2: "Permission denied"
**Symptoms**: Service account lacks permissions
**Solutions**:
1. **Go to** Google Cloud Console → IAM & Admin → IAM
2. **Find** your service account
3. **Edit** permissions
4. **Add** "Vision API User" role

#### Issue 3: "Billing not enabled"
**Symptoms**: API calls fail due to billing
**Solutions**:
1. **Go to** Google Cloud Console → Billing
2. **Verify** billing account is linked
3. **Check** billing account is active
4. **Confirm** project is linked to billing

#### Issue 4: "Quota exceeded"
**Symptoms**: Too many API requests
**Solutions**:
1. **Check** current usage: Google Cloud Console → APIs & Services → Quotas
2. **Request** quota increase if needed
3. **Implement** rate limiting in application
4. **Enable** fallback to free OCR

#### Issue 5: "Network connectivity"
**Symptoms**: API timeouts or connection errors
**Solutions**:
```bash
# Test internet connectivity
ping google.com

# Test Vision API endpoint
curl -I https://vision.googleapis.com

# Check firewall settings
# Ensure outbound HTTPS (port 443) is allowed
```

### Debug Mode

#### Enable Detailed Logging
```json
{
    "debug": {
        "enabled": true,
        "log_level": "DEBUG",
        "log_file": "google_vision_debug.log",
        "log_api_requests": true,
        "log_responses": false
    }
}
```

#### Command Line Debug
```bash
# Enable verbose output
python cli_ocr.py test_image.jpg -o output.txt --engine google_vision --verbose --debug

# Check debug log
type google_vision_debug.log
```

### Performance Issues

#### Slow API Responses
**Solutions**:
1. **Check** internet connection speed
2. **Reduce** image size/resolution
3. **Enable** local caching
4. **Use** concurrent processing for batches

#### Memory Issues
**Solutions**:
```json
{
    "memory_optimization": {
        "max_image_size_mb": 10,
        "resize_large_images": true,
        "target_dpi": 300,
        "cleanup_temp_files": true
    }
}
```

---

## 📞 **Support and Resources**

### Getting Help
- **OCR Document Converter Support**: Use Google Vision API tab in GUI settings
- **Google Cloud Support**: [Google Cloud Support](https://cloud.google.com/support)
- **API Documentation**: [Vision API Docs](https://cloud.google.com/vision/docs)
- **GitHub Issues**: [Report Problems](https://github.com/Beaulewis1977/quick_ocr_doc_converter/issues)

### Useful Resources
- **Pricing Calculator**: [Google Cloud Pricing](https://cloud.google.com/products/calculator)
- **API Limits**: [Vision API Quotas](https://cloud.google.com/vision/quotas)
- **Best Practices**: [Vision API Best Practices](https://cloud.google.com/vision/docs/best-practices)
- **Security Guide**: [API Key Security](https://cloud.google.com/docs/authentication/best-practices-applications)

### Quick Reference

#### Essential Commands
```bash
# Test API connection
python -c "from google.cloud import vision; print('✅ Google Vision API is ready')"

# Convert with Google Vision
python cli_ocr.py input.pdf -o output.txt --engine google_vision

# Convert with fallback
python cli_ocr.py input.pdf -o output.txt --engine google_vision --fallback

# Check usage
gcloud logging read "resource.type=gce_instance" --limit 50
```

#### Configuration Checklist
- [ ] Google Cloud project created
- [ ] Vision API enabled
- [ ] Billing account linked
- [ ] Service account created
- [ ] JSON key downloaded
- [ ] Environment variable set
- [ ] Application configured
- [ ] Connection tested
- [ ] Fallback verified

---

**🎉 Congratulations! You now have Google Vision API integrated with OCR Document Converter v3.1.0. Enjoy premium OCR quality with automatic fallback protection!**