# Makefile for UniversalConverter32.dll
# Builds 32-bit DLL for VB6/VFP9 compatibility

# Compiler settings
CXX = g++
CXXFLAGS = -m32 -O2 -std=c++17 -DWIN32 -D_WIN32 -DNDEBUG
LDFLAGS = -m32 -shared -Wl,--enable-stdcall-fixup -Wl,--kill-at

# Target and source files
TARGET = UniversalConverter32.dll
SOURCE = UniversalConverter32.cpp
DEF_FILE = UniversalConverter32.def

# Default target
all: $(TARGET)

# Build the DLL
$(TARGET): $(SOURCE) $(DEF_FILE)
	@echo Building $(TARGET)...
	$(CXX) $(CXXFLAGS) $(LDFLAGS) -o $(TARGET) $(SOURCE) $(DEF_FILE)
	@echo Build complete!
	@echo.
	@echo To use this DLL:
	@echo 1. Copy $(TARGET) to your VB6/VFP9 project directory
	@echo 2. Copy cli.py and supporting files to the same directory
	@echo 3. Ensure Python is installed and in PATH
	@echo 4. Use the VB6/VFP9 integration modules provided

# Clean build artifacts
clean:
	@echo Cleaning build artifacts...
	-del $(TARGET) 2>nul
	-del *.o 2>nul
	-del *.obj 2>nul
	@echo Clean complete!

# Install to system directory (requires admin)
install: $(TARGET)
	@echo Installing $(TARGET) to system...
	copy $(TARGET) %WINDIR%\System32\
	@echo Installation complete!

# Create distribution package
package: $(TARGET)
	@echo Creating distribution package...
	-mkdir dist 2>nul
	copy $(TARGET) dist\
	copy ..\cli.py dist\
	copy ..\requirements.txt dist\
	copy ..\VB6_UniversalConverter.bas dist\
	copy ..\UniversalConverter_VFP9.prg dist\
	copy README_DLL.md dist\
	@echo Package created in dist\ directory

# Test the DLL (requires test files)
test: $(TARGET)
	@echo Testing DLL functionality...
	@echo This requires manual testing with VB6/VFP9
	@echo See the integration examples in VB6_UniversalConverter.bas and UniversalConverter_VFP9.prg

.PHONY: all clean install package test