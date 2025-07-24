# 🚀 Modern Legacy Document Converter - Complete Project Specification

## 📋 Project Overview

Create a **modern, beautiful desktop application** for legacy document conversion using SvelteKit + Tailwind + Skeleton UI + Tauri. This replaces the existing Python-based system with a web-native, high-performance solution specifically designed for **legacy system integration** (VB6, VFP9, enterprise environments).

---

## 🎯 Tech Stack (EXACT REQUIREMENTS)

### **Frontend Stack:**
```json
{
  "framework": "SvelteKit",
  "styling": "Tailwind CSS",
  "ui_library": "Skeleton UI",
  "language": "TypeScript",
  "build_tool": "Vite",
  "animations": "Svelte transitions + CSS animations",
  "icons": "Lucide Svelte",
  "state_management": "Svelte stores"
}
```

### **Desktop Wrapper:**
```json
{
  "desktop_framework": "Tauri",
  "backend_language": "Rust",
  "bundle_size_target": "<20MB",
  "platforms": ["Windows", "macOS", "Linux"]
}
```

### **Document Processing (Rust Backend):**
```json
{
  "core_library": "pandoc bindings",
  "rtf_processing": "Custom Rust RTF parser",
  "docx_processing": "docx-rs crate",
  "markdown_processing": "pulldown-cmark",
  "file_system": "notify crate for folder monitoring"
}
```

---

## 🎨 UI/UX Requirements (CRITICAL FOR BEAUTY)

### **Design System:**
- **Theme**: Professional, clean, minimal (Linear/Vercel inspired)
- **Colors**: Skeleton UI's built-in theme system + custom legacy-focused palette
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

## 📄 Core Features (MUST IMPLEMENT)

### **Core Functions (EXACTLY What Your Friend Needs):**

#### **Primary Functions (Lightweight DLL - <5MB):**
```rust
// Core bidirectional conversion functions (THE MAIN REQUIREMENT)
1. Rtf2MD(input_rtf: String) -> String      // RTF → Markdown conversion
2. MD2Rtf(input_md: String) -> String       // Markdown → RTF conversion

// File-based versions for VB6/VFP9 compatibility  
3. ConvertRtfFileToMd(input_path: String, output_path: String) -> i32
4. ConvertMdFileToRtf(input_path: String, output_path: String) -> i32
```

#### **Essential Legacy Helper Functions:**
```rust
// Document validation (prevents crashes in legacy systems)
5. ValidateRtfDocument(rtf_content: String) -> i32    // Returns 1=valid, 0=invalid
6. ValidateMarkdownDocument(md_content: String) -> i32 // Returns 1=valid, 0=invalid

// Text processing utilities (common legacy needs)
7. ExtractPlainText(document_content: String, format: String) -> String
8. CleanRtfFormatting(rtf_content: String) -> String  // Remove complex formatting
9. NormalizeMarkdown(md_content: String) -> String    // Standardize markdown syntax

// Error handling (critical for VB6/VFP9)
10. GetLastError() -> String              // Detailed error messages
11. TestConnection() -> i32               // Returns 1 if DLL working, 0 if not
12. GetVersionInfo() -> String            // DLL version and build info
```

#### **Batch Processing (Legacy-Friendly):**
```rust
// Simple batch operations for legacy systems
13. ConvertFolderRtfToMd(input_folder: String, output_folder: String) -> i32
14. ConvertFolderMdToRtf(input_folder: String, output_folder: String) -> i32
15. GetBatchProgress() -> String          // JSON: {"processed": 5, "total": 10, "current": "file.rtf"}
16. CancelBatchOperation() -> i32         // Returns 1 if cancelled successfully
```

#### **Legacy Template System:**
```rust
// RTF template functionality (useful for legacy reports)  
17. ApplyRtfTemplate(content: String, template_path: String) -> String
18. CreateRtfTemplate(sample_rtf: String, template_name: String) -> i32
19. ListAvailableTemplates() -> String    // JSON array of template names

// Markdown template system
20. ApplyMarkdownTemplate(content: String, template_path: String) -> String
21. ValidateTemplate(template_path: String, format: String) -> i32
```

#### **Database Integration (Legacy Systems Love This):**
```rust
// Simple database export functions (common legacy need)
22. ExportToCSV(markdown_content: String, delimiter: String) -> String
23. ImportFromCSV(csv_content: String, delimiter: String) -> String  // Returns markdown
24. ConvertTableToRtf(csv_data: String) -> String         // Creates RTF table
25. ExtractTablesFromRtf(rtf_content: String) -> String   // Returns CSV format
```

### **Advanced Features:**
4. **Template System:**
   - RTF template management
   - Markdown template customization
   - Style preservation options
   - Custom conversion profiles

5. **File System Integration:**
   - Hot folder monitoring
   - Automatic conversion triggers
   - Network drive support
   - File association registration

6. **Enterprise Features:**
   - User configuration profiles
   - Logging and audit trails
   - Error notification system
   - Performance monitoring

---

## 🏗️ Application Architecture

### **Frontend Structure (SvelteKit):**
```
src/
├── lib/
│   ├── components/
│   │   ├── DragDropZone.svelte
│   │   ├── ProgressBar.svelte
│   │   ├── SettingsPanel.svelte
│   │   ├── FileCard.svelte
│   │   └── ThemeSelector.svelte
│   ├── stores/
│   │   ├── files.ts (file management)
│   │   ├── settings.ts (app configuration)
│   │   ├── theme.ts (dark/light mode)
│   │   └── conversion.ts (conversion state)
│   └── utils/
│       ├── file-validation.ts
│       ├── conversion-api.ts
│       └── legacy-integration.ts
├── routes/
│   └── +page.svelte (main app)
└── app.html
```

### **Backend Structure (Tauri/Rust):**
```
src-tauri/
├── src/
│   ├── main.rs
│   ├── conversion/
│   │   ├── mod.rs
│   │   ├── docx.rs
│   │   ├── rtf.rs
│   │   └── markdown.rs
│   ├── legacy/
│   │   ├── mod.rs
│   │   ├── vb6_integration.rs
│   │   └── file_system.rs
│   └── utils/
│       ├── file_monitor.rs
│       └── progress_tracker.rs
└── Cargo.toml
```

---

## 🎨 Visual Design Specifications

### **Color Palette (Skeleton UI + Custom):**
```css
/* Primary Colors */
--primary-50: #eff6ff;    /* Light blue backgrounds */
--primary-500: #3b82f6;   /* Main brand blue */
--primary-900: #1e3a8a;   /* Dark blue accents */

/* Legacy System Colors */
--legacy-amber: #f59e0b;   /* Warning/legacy indicators */
--legacy-green: #10b981;  /* Success states */
--legacy-red: #ef4444;    /* Error states */

/* Professional Grays */
--surface-50: #f8fafc;    /* Light backgrounds */
--surface-900: #0f172a;   /* Dark backgrounds */
```

### **Typography Scale:**
```css
/* Headings */
.h1 { font-size: 2.25rem; font-weight: 700; }  /* Main title */
.h2 { font-size: 1.875rem; font-weight: 600; } /* Section headers */
.h3 { font-size: 1.5rem; font-weight: 600; }   /* Subsections */

/* Body Text */
.text-base { font-size: 1rem; line-height: 1.5; }     /* Regular text */
.text-sm { font-size: 0.875rem; line-height: 1.4; }   /* Secondary text */
.text-xs { font-size: 0.75rem; line-height: 1.3; }    /* Labels */
```

### **Animation Specifications:**
```css
/* Smooth Transitions (CRITICAL) */
.transition-all { transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); }
.transition-colors { transition: color 0.15s ease-in-out; }
.transition-transform { transition: transform 0.15s ease-in-out; }

/* Hover Effects */
.hover-lift:hover { transform: translateY(-2px); }
.hover-scale:hover { transform: scale(1.02); }
```

---

## 🔧 Implementation Guidelines

### **Phase 1: Core MVP (Build This First)**
```typescript
// Essential components to build first:
1. Basic SvelteKit + Tauri setup
2. File drag-and-drop component
3. Basic DOCX → RTF → Markdown conversion
4. Simple progress indication
5. Dark/light theme toggle
```

### **Phase 2: Polish & Features**
```typescript
// Enhanced functionality:
1. Batch processing with queue management
2. Advanced settings panel
3. Template management system
4. Error handling and retry logic
5. Performance optimizations
```

### **Phase 3: Legacy Integration**
```typescript
// Legacy system features:
1. VB6/VFP9 COM integration
2. File system monitoring
3. Registry configuration
4. Command-line interface
5. Enterprise deployment features
```

---

## 📱 Sample Component Specifications

### **DragDropZone.svelte Example:**
```svelte
<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { fade, scale } from 'svelte/transition';
  
  let isDragOver = false;
  let files: File[] = [];
  
  const dispatch = createEventDispatcher();
  
  // Drag and drop handlers with beautiful animations
  function handleDrop(event: DragEvent) {
    // File processing logic with smooth state transitions
  }
</script>

<div 
  class="drag-zone {isDragOver ? 'drag-over' : ''}"
  class:has-files={files.length > 0}
  on:drop={handleDrop}
  on:dragover|preventDefault
  transition:scale
>
  <!-- Beautiful drop zone UI with Skeleton components -->
</div>

<style>
  .drag-zone {
    @apply border-2 border-dashed border-surface-300 dark:border-surface-600;
    @apply rounded-lg p-8 text-center transition-all duration-200;
    @apply hover:border-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/10;
  }
  
  .drag-over {
    @apply border-primary-500 bg-primary-100 dark:bg-primary-900/20;
    @apply scale-102 shadow-lg;
  }
</style>
```

---

## 🎯 Success Criteria

### **Performance Targets:**
- **Bundle Size**: < 20MB total application
- **Startup Time**: < 2 seconds cold start
- **Conversion Speed**: Process 100 documents in < 30 seconds
- **Memory Usage**: < 200MB during heavy processing

### **UI/UX Quality:**
- **Smooth Animations**: 60fps throughout
- **Responsive Design**: Works at 1024x768 minimum
- **Theme Consistency**: Perfect dark/light mode
- **Professional Appearance**: Indistinguishable from commercial software

### **Legacy Integration:**
- **VB6 Compatibility**: COM calls work perfectly
- **File System Integration**: Handles UNC paths, long paths
- **Enterprise Ready**: Logging, configuration, deployment
- **Error Handling**: Graceful degradation, clear error messages

---

## 📦 Deliverables

### **What to Build:**
1. **Complete SvelteKit application** with all specified components
2. **Tauri desktop wrapper** with Rust backend
3. **Document conversion engine** (Rust-based)
4. **Legacy integration layer** (COM, file system, registry)
5. **Build and deployment scripts** for all platforms
6. **User documentation** and installation guide

### **File Structure to Deliver:**
```
modern-legacy-converter/
├── src/                    # SvelteKit frontend
├── src-tauri/             # Tauri backend
├── docs/                  # Documentation
├── scripts/               # Build scripts
└── README.md             # Setup instructions
```

---

## 🚀 Getting Started Command

When you're ready to build this, start with:

```bash
# Initialize the project
npm create svelte@latest modern-legacy-converter
cd modern-legacy-converter
npm install

# Add required dependencies
npm install -D tailwindcss @tailwindcss/typography
npm install @skeletonlabs/skeleton lucide-svelte

# Initialize Tauri
npm install -D @tauri-apps/cli
npx tauri init

# Start development
npm run tauri dev
```

---

## 💡 Key Notes for Implementation

1. **Focus on Beauty First**: Make it look absolutely stunning before adding complex features
2. **Performance is Critical**: Legacy systems need fast, responsive applications  
3. **Test Early on Windows**: VB6/VFP9 integration must work perfectly
4. **Professional Polish**: Every animation, transition, and interaction should be smooth
5. **Modular Architecture**: Build components that can be easily extended

This specification gives you everything needed to build a **world-class legacy document converter** that will impress both modern developers and legacy system administrators! 🎯