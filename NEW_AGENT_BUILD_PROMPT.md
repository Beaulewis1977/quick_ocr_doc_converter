# 🚀 Build Prompt for New Agent

## **Your Mission:**
Build **LegacyBridge** - a modern, beautiful RTF ↔ Markdown converter for legacy systems using SvelteKit + Tailwind + Skeleton UI + Tauri.

## 🛠️ **Required Tools & Methodology:**

### **Essential Development Tools (USE THESE):**
- **Context7 MCP Server** - Use for deep codebase research and understanding existing patterns
- **Playwright** - For comprehensive E2E testing and UI validation
- **Sequential Thinking** - Break down complex problems step-by-step systematically
- **Task Tool** - For research, file exploration, and code analysis
- **Grep/Search Tools** - Investigate existing patterns and implementations
- **WebFetch** - Research best practices and documentation
- **Multiple parallel tool calls** - Research efficiently by using tools in parallel

### **Mandatory Development Workflow:**
```
🔍 RESEARCH → 🧠 THINK → 📋 PLAN → 🧪 TEST → 💻 CODE → 🧪 TEST → 🔧 DEBUG → ✅ VALIDATE
```

#### **Phase Breakdown (FOLLOW EXACTLY):**

1. **🔍 RESEARCH PHASE**
   - Use Context7 MCP Server to understand RTF and Markdown formats deeply
   - Research existing RTF parsers and Markdown generators
   - Study SvelteKit + Skeleton UI best practices and patterns
   - Investigate Tauri desktop app architecture
   - Research TDD patterns for frontend and Rust development

2. **🧠 THINK HARD PHASE**
   - Use sequential thinking to break down RTF ↔ Markdown conversion complexity
   - Plan the exact RTF parsing strategy (control codes, formatting, structure)
   - Design the Markdown generation algorithms
   - Think through edge cases and error scenarios
   - Consider performance implications and optimization strategies

3. **📋 PLAN THOROUGHLY PHASE**
   - Create detailed component architecture diagrams
   - Plan the exact UI component hierarchy and data flow
   - Design the Rust module structure and function signatures
   - Plan comprehensive test strategies (unit, integration, E2E)
   - Create detailed implementation milestones

4. **🧪 TEST-DRIVEN DEVELOPMENT (MANDATORY)**
   - **Write tests FIRST** - Before implementing any functionality
   - **Red-Green-Refactor cycle** - Failing test → working code → clean code
   - **Unit tests**: Test individual RTF parsing functions
   - **Integration tests**: Test full conversion workflows
   - **E2E tests**: Use Playwright to test UI interactions
   - **Continuous validation**: Run tests after every change

5. **💻 CODE WITH EXCELLENCE**
   - Follow the exact specifications in LEGACYBRIDGE_BUILD_SPEC.md
   - Use TypeScript throughout (no plain JavaScript)
   - Implement proper error handling with Result types
   - Write clean, maintainable, well-documented code
   - Follow Rust best practices for performance and safety

6. **🔧 SYSTEMATIC DEBUGGING**
   - Use proper debugging tools and comprehensive logging
   - Test conversion fidelity with real RTF and Markdown documents
   - Validate UI responsiveness and animation smoothness
   - Debug memory usage and performance bottlenecks
   - Test cross-platform compatibility

7. **✅ COMPREHENSIVE VALIDATION**
   - Validate all 25 functions work correctly
   - Test RTF → MD → RTF roundtrip fidelity
   - Validate UI meets professional commercial standards
   - Test VB6/VFP9 DLL compatibility
   - Performance validation (speed, memory, bundle size)

### **Testing Strategy (NON-NEGOTIABLE):**
```typescript
// Required test structure:
tests/
├── unit/
│   ├── rtf-parser.test.ts       // Test RTF parsing logic
│   ├── markdown-generator.test.ts // Test MD generation
│   └── validation.test.ts       // Test document validation
├── integration/
│   ├── conversion.test.ts       // Test full RTF ↔ MD workflows
│   └── batch-processing.test.ts // Test multi-file processing
└── e2e/
    ├── ui-interactions.spec.ts  // Playwright UI tests
    ├── drag-drop.spec.ts        // Test drag-drop functionality
    └── theme-switching.spec.ts  // Test dark/light themes
```

### **Quality Gates (MUST PASS):**
- ✅ All unit tests passing (95%+ coverage)
- ✅ All integration tests passing
- ✅ All Playwright E2E tests passing
- ✅ RTF conversion fidelity >95%
- ✅ UI animations smooth 60fps
- ✅ Professional commercial appearance
- ✅ Bundle size <20MB
- ✅ Conversion speed <1 second per document

---

## 📋 **EXACT INSTRUCTIONS:**

### **Step 1: Read the Complete Specification**
- Read `LEGACYBRIDGE_BUILD_SPEC.md` thoroughly
- This contains ALL technical requirements, UI designs, and function specifications
- Follow it exactly - every detail matters

### **Step 2: Build Phase 1 MVP (Start Here)**
Create a working prototype with these **exact features**:

#### **Frontend (SvelteKit + Skeleton UI):**
```typescript
// Required components to build:
1. DragDropZone.svelte - Beautiful file drop area with animations
2. ConversionProgress.svelte - Smooth progress bars with ETA
3. FileList.svelte - Show selected files with remove options
4. SettingsPanel.svelte - Basic settings with theme toggle
5. Main layout with professional styling (Linear/Vercel inspired)
```

#### **Backend (Tauri + Rust):**
```rust
// Required functions to implement FIRST:
1. convert_rtf_to_md(rtf_content: String) -> Result<String, String>
2. convert_md_to_rtf(md_content: String) -> Result<String, String>
3. convert_file(input_path: String, output_path: String) -> Result<(), String>
4. validate_document(content: String, format: String) -> bool
```

#### **UI Requirements (CRITICAL):**
- **Beautiful Design**: Use Skeleton UI components with Tailwind
- **Smooth Animations**: 60fps drag-drop, progress bars, transitions
- **Dark/Light Themes**: Professional color scheme with theme toggle
- **Responsive Layout**: Works at different window sizes
- **Professional Typography**: Inter font, clean spacing

### **Step 3: Technical Implementation**

#### **Initialize Project:**
```bash
# Start with these exact commands:
npm create svelte@latest legacybridge --template skeleton --types checkjs --prettier --eslint
cd legacybridge
npm install

# Add required dependencies:
npm install -D tailwindcss @tailwindcss/typography autoprefixer
npm install @skeletonlabs/skeleton @skeletonlabs/tw-plugin
npm install lucide-svelte

# Add Tauri:
npm install -D @tauri-apps/cli
npx tauri init
```

#### **Rust Backend Structure:**
```rust
// Create these modules in src-tauri/src/
- main.rs (Tauri setup)
- conversion/mod.rs (RTF ↔ Markdown conversion)
- conversion/rtf_parser.rs (RTF parsing logic)
- conversion/markdown_generator.rs (Markdown generation)
- utils/validation.rs (Document validation)
```

### **Step 4: Conversion Engine Logic**

#### **RTF to Markdown Strategy:**
```rust
// Implement RTF parsing with these priorities:
1. Basic text extraction (paragraphs, line breaks)
2. Bold/italic formatting (\\b, \\i)
3. Headers and structure
4. Lists (numbered and bullet)
5. Tables (if time permits)

// Convert to clean Markdown:
- **bold** and *italic* formatting
- # Headers (H1-H6)
- - Lists and 1. numbered lists
- Clean paragraph breaks
```

#### **Markdown to RTF Strategy:**
```rust
// Parse Markdown and generate RTF:
1. Parse with pulldown-cmark
2. Generate RTF control codes:
   - {\\rtf1 document structure
   - \\b bold \\b0 for bold text
   - \\i italic \\i0 for italic
   - \\par for paragraphs
3. Handle edge cases and validation
```

### **Step 5: UI Implementation Priority**

#### **Build in This Order:**
1. **Basic Layout** - Header, main area, status bar
2. **File Drop Zone** - Large, prominent, animated
3. **Conversion Logic** - Wire up Rust backend
4. **Progress Display** - Real-time conversion feedback
5. **Settings Panel** - Theme toggle, basic options
6. **Error Handling** - Beautiful error messages
7. **Polish** - Animations, responsive design

---

## 🎯 **Success Criteria for MVP:**

### **Functionality:**
- ✅ Drag RTF file → Get Markdown output
- ✅ Drag Markdown file → Get RTF output
- ✅ Batch processing (multiple files)
- ✅ Error handling with clear messages
- ✅ Progress indication during conversion

### **UI Quality:**
- ✅ Looks professional (commercial software quality)
- ✅ Smooth 60fps animations
- ✅ Perfect dark/light theme switching
- ✅ Responsive at different sizes
- ✅ No UI glitches or lag

### **Performance:**
- ✅ Fast conversion (<1 second for typical documents)
- ✅ Small app size (<20MB)
- ✅ Quick startup (<2 seconds)
- ✅ Smooth UI interactions

---

## 🚨 **CRITICAL REQUIREMENTS:**

### **Must Follow Exactly:**
1. **Use Skeleton UI components** - Don't build custom components
2. **Follow the 25-function specification** - These are what legacy systems need
3. **Professional visual design** - This must look like commercial software
4. **Perfect error handling** - No crashes, clear error messages
5. **Smooth animations** - 60fps throughout the interface

### **RTF Conversion Quality:**
- **Preserve formatting** - Bold, italic, headers, lists
- **Handle edge cases** - Malformed RTF, empty documents
- **Generate clean Markdown** - CommonMark compliant
- **Bidirectional fidelity** - RTF→MD→RTF should be nearly identical

### **Code Quality:**
- **TypeScript throughout** - No plain JavaScript
- **Proper error handling** - Result types, try/catch
- **Clean architecture** - Separate concerns, modular design
- **Performance focused** - Fast rendering, efficient algorithms

---

## 📁 **Deliverables Expected:**

1. **Working SvelteKit application** with all MVP features
2. **Tauri desktop wrapper** with Rust conversion engine
3. **Beautiful UI** matching the specification design
4. **Complete RTF ↔ Markdown conversion** functionality
5. **Build instructions** and setup documentation

---

## 🎯 **Start Command - Research First!**

**MANDATORY: Begin with deep research before any coding:**

### **Phase 1: Intensive Research (Day 1)**
```bash
# 1. Use Context7 MCP Server to research RTF format specification
#    - Understand RTF control codes (\b, \i, \par, etc.)
#    - Study RTF document structure and formatting
#    - Research existing RTF parsing strategies

# 2. Research Markdown generation best practices
#    - Study CommonMark specification
#    - Investigate markdown-it and other parsers
#    - Research bidirectional conversion challenges

# 3. Use Task tool to analyze SvelteKit + Skeleton UI patterns
#    - Research drag-drop implementations
#    - Study animation and transition patterns
#    - Investigate Tauri + SvelteKit integration examples

# 4. Research TDD patterns for Rust and TypeScript
#    - Study testing frameworks (Jest, vitest, Playwright)
#    - Research mocking strategies for file operations
#    - Investigate property-based testing for conversion fidelity
```

### **Phase 2: Deep Planning (Day 1-2)**
```bash
# 1. Use sequential thinking to break down RTF parsing:
#    - Token identification and parsing
#    - Control code interpretation
#    - Formatting state management
#    - Error handling and recovery

# 2. Plan the exact UI component architecture:
#    - Component hierarchy and data flow
#    - State management strategy
#    - Animation and transition timing
#    - Theme system implementation

# 3. Design comprehensive test strategy:
#    - Unit test coverage for all parsing functions
#    - Integration tests for full workflows
#    - E2E tests for user interactions
#    - Performance and fidelity validation
```

### **Phase 3: TDD Implementation (Day 2+)**
```bash
# 1. Set up project with testing infrastructure FIRST
npm create svelte@latest legacybridge --template skeleton
cd legacybridge
npm install -D vitest @testing-library/svelte playwright

# 2. Write failing tests for RTF parsing
# 3. Implement minimal code to make tests pass
# 4. Refactor and optimize
# 5. Repeat for each feature

# 6. Use Playwright for E2E validation throughout
```

### **Research Questions to Answer BEFORE Coding:**
1. **RTF Format**: What are the exact control codes for bold, italic, headers, lists?
2. **Markdown Generation**: How to ensure CommonMark compliance?
3. **State Management**: How to track formatting state during RTF parsing?
4. **Error Handling**: What are common RTF malformation patterns?
5. **Performance**: What are optimal parsing strategies for large documents?
6. **UI Architecture**: How to structure components for smooth animations?
7. **Testing**: How to test file conversion workflows effectively?

### **Success Criteria for Research Phase:**
- ✅ Deep understanding of RTF format specification
- ✅ Clear plan for bidirectional conversion algorithm
- ✅ Detailed UI component architecture designed
- ✅ Comprehensive test strategy documented
- ✅ Implementation milestones clearly defined

**Remember: Research and planning are MORE IMPORTANT than rushing to code. Spend 30% of your time researching, 20% planning, 50% implementing with TDD.**

**Your goal: Create a working, beautiful RTF ↔ Markdown converter that looks and feels like professional commercial software through systematic research, planning, and TDD.**

Focus on **quality over quantity** - make fewer features that work perfectly rather than many features that are buggy.

**Start with research, think systematically, test everything, then code with confidence!** 🚀