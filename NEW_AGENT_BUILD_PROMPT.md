# 🚀 LegacyBridge - Complete Build Prompt for New Agent

## **Your Mission:**
Build **LegacyBridge** - a modern, beautiful RTF ↔ Markdown converter for legacy systems using **Next.js + shadcn/ui + Tauri + Rust**.

---

## 🛠️ **Required Tools & Methodology:**

### **Essential Development Tools (USE THESE):**
- **Context7 MCP Server** - Deep codebase research and understanding existing patterns
- **Playwright** - Comprehensive E2E testing and UI validation
- **Sequential Thinking** - Break down complex problems step-by-step systematically
- **Task Tool** - Research, file exploration, and code analysis
- **Grep/Search Tools** - Investigate existing patterns and implementations
- **WebFetch** - Research best practices and documentation
- **Multiple parallel tool calls** - Research efficiently by using tools in parallel
- **TodoWrite** - Master todo list management (CRITICAL)

### **Mandatory Project Management:**
```
📋 PLAN → 🔍 RESEARCH → 🧠 THINK → 🧪 TEST → 💻 CODE → ✅ UPDATE → 🔄 REPEAT
```

#### **CRITICAL: Todo List Management**
1. **Create ONE master todo list** using TodoWrite at project start
2. **Update immediately** when finishing any task
3. **Add new tasks** as you discover them during development
4. **Work in small chunks** - each todo should be completable in 30-60 minutes
5. **Mark completed tasks** the moment you finish them
6. **Never have multiple todo lists** - use ONE master list only

---

## 📋 **Phase 1: Project Setup (MANDATORY FIRST STEPS)**

### **Step 1: Create Master Project Documentation**
```bash
# 1. Create CLAUDE.md file first (see template below)
# 2. Create HANDOFF_LOG.md for session tracking
# 3. Read LEGACYBRIDGE_BUILD_SPEC.md thoroughly
# 4. Create master todo list using TodoWrite
```

### **Step 2: Initialize Todo Management**
Create a comprehensive todo list with these exact categories:
```typescript
// Use TodoWrite to create this structure:
- [SETUP] Initialize Next.js + Tauri project structure
- [SETUP] Configure shadcn/ui and dependencies
- [SETUP] Set up testing infrastructure (Playwright, Jest)
- [RESEARCH] Deep dive RTF format specification
- [RESEARCH] Study Markdown generation best practices
- [CORE] Implement basic RTF parser in Rust
- [CORE] Implement Markdown generator
- [CORE] Create RTF→MD conversion function
- [CORE] Create MD→RTF conversion function
- [UI] Build DragDropZone component with shadcn/ui
- [UI] Create ConversionProgress component
- [UI] Implement theme switching (dark/light)
- [TESTING] Write unit tests for conversion functions
- [TESTING] Create E2E tests with Playwright
- [DLL] Export 32-bit DLL for VB6/VFP9
- [DOCS] Update handoff documentation
```

### **Step 3: Research Phase (30% of total time)**
Use multiple tools in parallel to research:

```bash
# Use Context7 MCP Server for deep research:
- RTF format specification and control codes
- CommonMark and GFM Markdown standards
- Next.js + Tauri integration patterns
- shadcn/ui component best practices
- Rust RTF parsing strategies

# Use WebFetch for documentation:
- Tauri desktop app architecture
- Framer Motion animation patterns
- TypeScript best practices for React
- TDD patterns for Rust and TypeScript

# Use Task tool for codebase analysis:
- Study existing RTF parsers
- Analyze Markdown generation libraries
- Research drag-drop implementations
```

---

## 🎯 **Development Rules (FOLLOW EXACTLY)**

### **🔄 Small Chunk Development:**
1. **Pick ONE todo item** at a time
2. **Complete it fully** (code + test + document)
3. **Update todo list immediately** using TodoWrite
4. **Commit changes** with descriptive message
5. **Repeat** - never work on multiple todos simultaneously

### **🌐 Codebase-Wide Consistency:**
1. **Before making changes**, search entire codebase for similar patterns
2. **Update ALL related files** when changing interfaces or types
3. **Run tests after every change** to ensure nothing breaks
4. **Use TypeScript strictly** - no `any` types allowed
5. **Follow existing naming conventions** throughout codebase

### **📝 Documentation Requirements:**
1. **Update HANDOFF_LOG.md** at end of each session
2. **Document ALL decisions** and reasoning
3. **Create inline comments** for complex logic
4. **Update README** as features are completed
5. **Maintain API documentation** for all 25 functions

---

## 🔧 **Tech Stack Implementation (EXACT)**

### **Frontend Setup:**
```bash
# Initialize project (EXACT commands):
npx create-next-app@latest legacybridge --typescript --tailwind --eslint --app --src-dir
cd legacybridge

# Install required dependencies:
npm install lucide-react framer-motion @radix-ui/react-slot class-variance-authority clsx tailwind-merge
npm install -D @tauri-apps/cli @types/node

# Set up shadcn/ui:
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card progress badge alert-dialog dropdown-menu switch

# Set up testing:
npm install -D @playwright/test vitest @testing-library/react @testing-library/jest-dom
```

### **Tauri Backend Setup:**
```bash
# Initialize Tauri:
npx tauri init

# Configure Rust dependencies in Cargo.toml:
[dependencies]
serde = { version = "1.0", features = ["derive"] }
tauri = { version = "1.0", features = ["api-all"] }
pulldown-cmark = "0.9"
comrak = "0.18"
```

### **Project Structure (CREATE EXACTLY):**
```
legacybridge/
├── CLAUDE.md                     # Agent rules and guidelines
├── HANDOFF_LOG.md                # Session tracking
├── src/
│   ├── components/
│   │   ├── ui/                   # shadcn/ui components
│   │   ├── DragDropZone.tsx
│   │   ├── ConversionProgress.tsx
│   │   ├── SettingsPanel.tsx
│   │   └── ThemeProvider.tsx
│   ├── lib/
│   │   ├── utils.ts              # Utility functions
│   │   └── tauri-api.ts          # Tauri bindings
│   ├── app/
│   │   ├── page.tsx              # Main application
│   │   ├── layout.tsx            # Root layout
│   │   └── globals.css           # Global styles
│   └── types/
│       └── index.ts              # TypeScript definitions
├── src-tauri/
│   ├── src/
│   │   ├── main.rs
│   │   ├── conversion/
│   │   │   ├── mod.rs
│   │   │   ├── rtf_parser.rs
│   │   │   └── markdown_generator.rs
│   │   └── commands.rs           # Tauri commands
│   └── Cargo.toml
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── docs/
    └── API.md                    # Function documentation
```

---

## 🧪 **Testing Strategy (NON-NEGOTIABLE)**

### **Test-Driven Development:**
```typescript
// 1. Write failing test FIRST
// 2. Implement minimal code to pass
// 3. Refactor and improve
// 4. Update todo list

// Required test structure:
tests/
├── unit/
│   ├── rtf-parser.test.ts       # Test RTF parsing logic
│   ├── markdown-gen.test.ts     # Test MD generation
│   └── validation.test.ts       # Test document validation
├── integration/
│   ├── conversion.test.ts       # Test full RTF ↔ MD workflows
│   └── batch-processing.test.ts # Test multi-file processing
└── e2e/
    ├── drag-drop.spec.ts        # Playwright UI tests
    ├── conversion-ui.spec.ts    # Test conversion interface
    └── settings.spec.ts         # Test settings panel
```

### **Quality Gates (MUST PASS):**
- ✅ All unit tests passing (90%+ coverage)
- ✅ All integration tests passing
- ✅ All Playwright E2E tests passing
- ✅ RTF conversion fidelity >95%
- ✅ UI animations smooth 60fps
- ✅ No TypeScript errors
- ✅ Bundle size ~15MB

---

## 📊 **Progress Tracking Requirements**

### **Master Todo List Management:**
1. **Use TodoWrite tool** for ALL todo management
2. **Update immediately** after completing each task
3. **Add estimated time** for each new task
4. **Track blockers** and dependencies
5. **Never duplicate todos** - maintain ONE source of truth

### **Session Handoff Documentation:**
Create HANDOFF_LOG.md with this format:
```markdown
# LegacyBridge Development Log

## Session [DATE] [TIME] - [DURATION]

### Completed This Session:
- ✅ [Task description] - [time taken]
- ✅ [Task description] - [time taken]

### Current Status:
- 🔄 [In progress task]
- ⏸️ [Blocked task] - [reason]

### Next Session Priorities:
1. [High priority task]
2. [Medium priority task]
3. [Low priority task]

### Technical Decisions Made:
- [Decision] - [reasoning]
- [Decision] - [reasoning]

### Issues/Blockers:
- [Issue description] - [proposed solution]

### Files Modified:
- src/components/DragDropZone.tsx
- src-tauri/src/conversion/rtf_parser.rs

### Next Agent Should Know:
- [Important context for continuation]
```

---

## 🎯 **Core Function Priorities**

### **Priority 1 (Week 1): Core MVP**
```rust
// Implement these 7 functions FIRST:
1. Rtf2MD(input_rtf: String) -> String           // RTF → Markdown
2. MD2Rtf(input_md: String) -> String            // Markdown → RTF  
3. ConvertRtfFileToMd(input_path: String, output_path: String) -> i32
4. ConvertMdFileToRtf(input_path: String, output_path: String) -> i32
5. GetLastError() -> String                      // Error messages
6. TestConnection() -> i32                       // Health check
7. GetVersionInfo() -> String                    // Version info
```

### **Priority 2 (Week 2): UI Components**
```typescript
// Build these components with shadcn/ui:
1. DragDropZone - Beautiful file drop with animations
2. ConversionProgress - Smooth progress bars
3. FileList - Display selected files with actions
4. SettingsPanel - Configuration options
5. ThemeProvider - Dark/light mode switching
```

### **Priority 3 (Week 3): Advanced Features**
```rust
// Add remaining functions:
8-16. Document validation and text processing utilities
17-21. Template system for RTF/Markdown templates
22-25. CSV integration for database workflows
```

---

## 🚀 **Start Commands (EXECUTE FIRST)**

### **Initial Setup Sequence:**
```bash
# 1. Create project structure
npx create-next-app@latest legacybridge --typescript --tailwind --eslint --app --src-dir
cd legacybridge

# 2. Set up dependencies (ALL required)
npm install lucide-react framer-motion @radix-ui/react-slot class-variance-authority clsx tailwind-merge
npm install -D @tauri-apps/cli @playwright/test vitest @testing-library/react

# 3. Initialize shadcn/ui
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card progress badge alert-dialog switch

# 4. Set up Tauri
npx tauri init

# 5. Create CLAUDE.md and HANDOFF_LOG.md files
```

### **Development Workflow:**
```bash
# Every development session:
1. Read CLAUDE.md rules
2. Review HANDOFF_LOG.md for context
3. Check master todo list
4. Pick ONE small task
5. Research → Plan → Test → Code → Update todos
6. Update handoff log before ending session
```

---

## ✅ **Success Criteria**

### **Technical Requirements:**
- **Perfect RTF ↔ Markdown conversion** with 95%+ fidelity
- **Beautiful shadcn/ui interface** that looks commercial-grade
- **32-bit DLL export** for VB6/VFP9 compatibility
- **All 25 functions implemented** and tested
- **Smooth 60fps animations** throughout UI
- **~15MB total bundle size**

### **Development Quality:**
- **Complete test coverage** (unit + integration + E2E)
- **Comprehensive documentation** for all functions
- **Consistent code style** throughout codebase
- **Professional git commit history**
- **Detailed handoff documentation**

### **User Experience:**
- **Drag-and-drop file handling** with visual feedback
- **Real-time conversion progress** with ETA
- **Dark/light theme switching** 
- **Intuitive settings panel**
- **Error handling with clear messages**

---

## 🎯 **Remember:**

1. **Work in small chunks** - 30-60 minute tasks only
2. **Update todos immediately** after each completion
3. **Test everything** - no untested code
4. **Document decisions** in handoff log
5. **Use parallel tools** for efficient research
6. **Maintain codebase consistency** across all changes
7. **Focus on visual quality** - this must impress VB6/VFP9 developers

**Your goal: Build a stunning, professional RTF ↔ Markdown converter that replaces Pandoc's 100MB bloat with a 5MB focused solution while providing a world-class modern interface.**

Start with the CLAUDE.md creation, then dive into research! 🚀