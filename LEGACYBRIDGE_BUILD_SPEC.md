# 🌉 LegacyBridge - Complete Build Specification

**A modern, beautiful RTF ↔ Markdown converter specifically designed for legacy systems (VB6, VFP9)**

---

## 📋 Project Overview

**LegacyBridge** solves the exact problem your friend described: replacing Pandoc's bloated 100MB solution with a lightweight, focused RTF ↔ Markdown converter that works perfectly with 32-bit legacy programming environments.

### **Core Mission:**
- **Lightweight DLL**: <5MB (vs Pandoc's 100MB)
- **Bidirectional Conversion**: RTF ↔ Markdown with perfect fidelity
- **Legacy Compatible**: VB6/VFP9 friendly function signatures
- **Modern GUI**: Beautiful Next.js + shadcn/ui interface for ease of use
- **Professional Quality**: Enterprise-grade reliability and error handling

---

## 🎯 Application Name & Branding

### **Name: LegacyBridge**
- **Tagline**: "Bridging Modern and Legacy Document Systems"
- **Logo Concept**: Modern bridge icon connecting two document formats
- **Color Scheme**: Professional blue/gray with legacy-gold accents

---

## 🔧 Tech Stack (EXACT REQUIREMENTS)

### **Frontend (Modern GUI):**
```json
{
  "framework": "Next.js",
  "styling": "Tailwind CSS",
  "ui_library": "shadcn/ui + Radix UI",
  "language": "TypeScript", 
  "build_tool": "Next.js built-in",
  "animations": "Framer Motion",
  "icons": "Lucide React",
  "desktop_wrapper": "Tauri",
  "target_size": "~15MB total app"
}
```

### **Desktop Wrapper:**
```json
{
  "desktop_framework": "Tauri",
  "backend_language": "Rust",
  "bundle_size_target": "~15MB",
  "platforms": ["Windows", "macOS", "Linux"]
}
```

### **Document Processing (Rust Backend):**
```json
{
  "core_library": "Custom RTF parser (lightweight)",
  "rtf_processing": "Custom Rust RTF parser",
  "markdown_processing": "pulldown-cmark + comrak",
  "dll_export": "Windows 32-bit DLL with C ABI",
  "target_size": "<5MB DLL only"
}
```

---

## 🎨 UI/UX Requirements (CRITICAL FOR BEAUTY)

### **Design System:**
- **Theme**: Professional, clean, minimal (Linear/Vercel inspired)
- **Colors**: shadcn/ui's built-in theme system + custom legacy-focused palette
- **Typography**: Inter font family (modern, readable)
- **Spacing**: Consistent 4px grid system
- **Animations**: Smooth, 60fps, subtle (not distracting)

### **Core UI Components Needed:**

#### **1. File Drag-and-Drop Zone**
```typescript
// Required features:
- Large, prominent drop area with dashed border
- Animated hover states (border color change, scale effect)
- File type validation with visual feedback
- Multiple file selection support
- Beautiful file preview cards with thumbnails
- Remove/replace file functionality
```

#### **2. Document Conversion Progress**
```typescript
// Required features:
- Animated progress bars (smooth filling animation)
- File-by-file progress indicators
- Overall batch progress
- ETA calculations and display
- Success/error states with icons
- Conversion speed statistics
```

#### **3. Settings Panel**
```typescript
// Required features:
- Collapsible sidebar or modal
- Toggle switches for options (with smooth animations)
- Dropdown selectors for formats
- Input fields for paths and templates
- Theme switcher (dark/light toggle)
- Save/load configuration profiles
```

#### **4. Professional Layout**
```typescript
// Required structure:
- Header with logo and theme toggle
- Main content area with drag-drop
- Sidebar for settings (collapsible)  
- Footer with status information
- Responsive design (works at different window sizes)
```

---

## 🎯 Complete Function List (25 Functions)

### **🔥 Core Functions (Priority 1 - Build These First):**
```rust
// THE MAIN REQUIREMENT - Your friend's exact needs
1. Rtf2MD(input_rtf: String) -> String           // RTF → Markdown
2. MD2Rtf(input_md: String) -> String            // Markdown → RTF
3. ConvertRtfFileToMd(input_path: String, output_path: String) -> i32
4. ConvertMdFileToRtf(input_path: String, output_path: String) -> i32

// Essential error handling for VB6/VFP9
5. GetLastError() -> String                      // Detailed error messages
6. TestConnection() -> i32                       // Returns 1=working, 0=error
7. GetVersionInfo() -> String                    // DLL version info
```

### **🛡️ Document Validation (Priority 2):**
```rust
// Prevent crashes in legacy systems
8. ValidateRtfDocument(rtf_content: String) -> i32    // 1=valid, 0=invalid
9. ValidateMarkdownDocument(md_content: String) -> i32 // 1=valid, 0=invalid
10. ExtractPlainText(document: String, format: String) -> String
```

### **📁 Batch Processing (Priority 3):**
```rust
// Legacy systems love batch operations
11. ConvertFolderRtfToMd(input_folder: String, output_folder: String) -> i32
12. ConvertFolderMdToRtf(input_folder: String, output_folder: String) -> i32
13. GetBatchProgress() -> String                 // JSON progress data
14. CancelBatchOperation() -> i32                // Cancel current batch
```

### **🎨 Text Processing Utilities (Priority 3):**
```rust
// Common legacy text processing needs  
15. CleanRtfFormatting(rtf_content: String) -> String    // Remove complex formatting
16. NormalizeMarkdown(md_content: String) -> String      // Standardize syntax
```

### **📋 Template System (Priority 4):**
```rust
// RTF templates for reports (legacy systems love this)
17. ApplyRtfTemplate(content: String, template_path: String) -> String
18. CreateRtfTemplate(sample_rtf: String, template_name: String) -> i32
19. ListAvailableTemplates() -> String           // JSON array
20. ApplyMarkdownTemplate(content: String, template_path: String) -> String
21. ValidateTemplate(template_path: String, format: String) -> i32
```

### **🗄️ Database Integration (Priority 4):**
```rust
// Legacy database integration (common need)
22. ExportToCSV(markdown_content: String, delimiter: String) -> String
23. ImportFromCSV(csv_content: String, delimiter: String) -> String
24. ConvertTableToRtf(csv_data: String) -> String        // CSV → RTF table
25. ExtractTablesFromRtf(rtf_content: String) -> String  // RTF → CSV
```

---

## 🏗️ MVP Build Phases

### **Phase 1: Core MVP (Week 1-2)**
**Goal**: Basic working RTF ↔ Markdown conversion
```typescript
// Build these components first:
1. Basic Next.js + Tauri setup
2. Simple drag-drop file interface  
3. Core Rust functions: Rtf2MD, MD2Rtf, ConvertFiles
4. Basic error handling and validation
5. Simple progress indication
```

### **Phase 2: Polish MVP (Week 3)**
**Goal**: Professional UI and batch processing
```typescript
// Add these features:
1. Beautiful shadcn/ui components
2. Dark/light theme switching
3. Batch file processing
4. Enhanced error messages
5. Settings panel with basic options
```

### **Phase 3: Legacy Integration (Week 4)**
**Goal**: VB6/VFP9 DLL compatibility
```typescript
// Focus on legacy compatibility:
1. 32-bit DLL export with C ABI
2. All 25 functions implemented
3. Template system for reports
4. Database CSV integration
5. Complete error handling
```

---

## 🎯 File Structure Template

```
legacybridge/
├── src/                           # Next.js frontend
│   ├── components/
│   │   ├── ui/                    # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── progress.tsx
│   │   │   └── ...
│   │   ├── DragDropZone.tsx
│   │   ├── ConversionProgress.tsx
│   │   ├── SettingsPanel.tsx
│   │   ├── FileList.tsx
│   │   └── ThemeToggle.tsx
│   ├── lib/
│   │   ├── stores/
│   │   │   ├── files.ts
│   │   │   ├── conversion.ts
│   │   │   └── settings.ts
│   │   └── utils/
│   │       ├── file-validation.ts
│   │       └── tauri-api.ts
│   ├── app/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   └── globals.css
│   └── components.json              # shadcn/ui config
├── src-tauri/                     # Rust backend
│   ├── src/
│   │   ├── main.rs
│   │   ├── conversion/
│   │   │   ├── mod.rs
│   │   │   ├── rtf_parser.rs
│   │   │   └── markdown_generator.rs
│   │   ├── dll/
│   │   │   ├── mod.rs
│   │   │   └── exports.rs         # 25 exported functions
│   │   └── utils/
│   │       ├── validation.rs
│   │       └── error_handling.rs
│   └── Cargo.toml
├── templates/                     # RTF/MD templates
├── examples/                      # VB6/VFP9 integration examples
└── README.md
```

---

## 🚀 Success Criteria

### **Performance Targets:**
- **DLL Size**: <5MB (vs Pandoc's 100MB)
- **App Bundle**: ~15MB total
- **Conversion Speed**: <500ms for typical documents
- **Memory Usage**: <100MB during processing
- **Startup Time**: <2 seconds

### **Quality Targets:**
- **RTF Fidelity**: 95%+ formatting preservation
- **Markdown Standards**: CommonMark + GFM compatible
- **Error Handling**: No crashes, clear error messages
- **Legacy Compatibility**: Perfect VB6/VFP9 integration

### **UI Quality:**
- **Smooth Animations**: 60fps throughout
- **Professional Appearance**: Commercial software quality
- **Intuitive Interface**: No learning curve required
- **Responsive**: Works at different window sizes

---

## 💻 VB6 Integration Example

```vb
' VB6 Usage Example
Private Declare Function Rtf2MD Lib "legacybridge.dll" (ByVal rtf As String) As String
Private Declare Function MD2Rtf Lib "legacybridge.dll" (ByVal md As String) As String
Private Declare Function GetLastError Lib "legacybridge.dll" () As String

Private Sub ConvertDocument()
    Dim rtfContent As String
    Dim markdownResult As String
    
    ' Read RTF from file or database
    rtfContent = "{\\rtf1 Hello \\b World\\b0}"
    
    ' Convert to Markdown
    markdownResult = Rtf2MD(rtfContent)
    
    If markdownResult <> "" Then
        MsgBox "Success: " & markdownResult
    Else
        MsgBox "Error: " & GetLastError()
    End If
End Sub
```

---

## 🎯 Development Priorities

### **MUST HAVE (MVP):**
1. ✅ RTF ↔ Markdown bidirectional conversion
2. ✅ Beautiful drag-drop interface with shadcn/ui
3. ✅ Batch file processing
4. ✅ Dark/light themes
5. ✅ VB6/VFP9 compatible DLL

### **SHOULD HAVE (Post-MVP):**
1. ✅ Template system
2. ✅ CSV database integration
3. ✅ Advanced text processing
4. ✅ Settings profiles
5. ✅ Performance monitoring

### **NICE TO HAVE (Future):**
1. 🔮 Cloud storage integration
2. 🔮 Advanced RTF formatting options
3. 🔮 Markdown extensions
4. 🔮 Multi-language interface
5. 🔮 Plugin system

---

## 📋 Quick Start Commands

```bash
# Initialize the project
npx create-next-app@latest legacybridge --typescript --tailwind --eslint --app --src-dir
cd legacybridge

# Install dependencies
npm install lucide-react framer-motion @radix-ui/react-slot
npm install -D @tauri-apps/cli

# Install shadcn/ui
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card progress

# Initialize Tauri
npx tauri init

# Start development
npm run tauri dev
```

This specification provides everything needed to build **LegacyBridge** - a professional, lightweight solution that perfectly addresses your friend's needs while looking absolutely stunning! 🌉