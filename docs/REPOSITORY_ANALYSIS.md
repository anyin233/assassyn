# Assassyn Repository Analysis Report

## Executive Summary

**Assassyn** (**As**ynchronous **S**emantics for **A**rchitectural **S**imulation & **Syn**thesis) is a hardware design framework that provides a unified interface for both simulation and RTL (Verilog) generation. The project aims to unify hardware modeling, implementation, and verification under a single Python-based DSL.

---

## Dependency Analysis

### All Dependencies Are Publicly Available

After thorough analysis, **the repository does NOT rely on any non-published source code or proprietary binaries**. All dependencies are from public sources:

#### 1. Git Submodules (All Public)

| Component | Source | Purpose |
|-----------|--------|---------|
| **CIRCT** | https://github.com/llvm/circt | LLVM project for Verilog backend via PyCDE |
| **Verilator** | https://github.com/verilator/verilator | Open-source Verilog simulator |
| **Ramulator2** | https://github.com/CMU-SAFARI/ramulator2 | CMU's DRAM memory simulator |
| **Agentize** | https://github.com/synthesys-lab/agentize | AI-assisted development helper (public) |

#### 2. Python Dependencies (All from PyPI)
```
pytest == 7.4.3        # Testing framework
pylint == 3.2.3        # Code linting
pytest-xdist == 3.6.1  # Parallel test execution
nanobind == 2.7.0      # C++/Python bindings
cocotb == 1.9.2        # Coroutine-based cosimulation
numpy == 1.26.0        # Numerical computing
```

#### 3. Rust Dependencies (All from crates.io)
```toml
libloading = "0.7"   # Dynamic library loading
num-bigint = "0.4"   # Big integer support
num-traits = "0.2"   # Numeric trait definitions
rand = "0.8"         # Random number generation
```

#### 4. System Dependencies (Ubuntu packages)
- Build tools: `cmake`, `ninja-build`, `autoconf`, `flex`, `bison`, `ccache`
- Python: `python3-pip`, `python3-dev`, `python3-venv`, `pybind11-dev`
- C++: `build-essential`, `numactl`, `help2man`

---

## Architecture Overview

### Core Components

```
assassyn/
├── python/assassyn/          # Core Python Framework
│   ├── ir/                   # Intermediate Representation
│   │   ├── dtype.py          # Data type system
│   │   ├── expr/             # Expression nodes (arithmetic, arrays, calls)
│   │   ├── memory/           # SRAM/DRAM abstractions
│   │   └── module/           # Module definitions (Base, External, FSM)
│   ├── builder/              # AST construction utilities
│   ├── codegen/              # Code generation backends
│   │   ├── simulator/        # Rust simulator generation
│   │   └── verilog/          # Verilog/RTL via PyCDE
│   ├── analysis/             # IR analysis tools
│   └── frontend.py           # Python DSL frontend
├── tools/
│   ├── rust-sim-runtime/     # Rust simulation runtime
│   └── c-ramulator2-wrapper/ # C++ FFI wrapper for Ramulator2
├── 3rd-party/                # External dependencies (submodules)
├── examples/                 # 12+ example applications
└── tutorials/                # Educational Quarto documents
```

### Key Abstractions

1. **Credit-Based Pipeline Stages**: Modules operate with a credit counter system for flow control
2. **Driver Module**: Acts as the "main" function with infinite credits
3. **Trace-Based Python DSL**: Operator overloading for hardware description
4. **Dual-Target Generation**: Same code produces both Rust simulator and Verilog RTL

---

## How to Contribute to Assassyn

### Getting Started

1. **Fork the Repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/<your-username>/assassyn
   cd assassyn
   ```

2. **Initialize Submodules**
   ```bash
   git submodule update --init --recursive
   ```

3. **Set Up Development Environment**
   ```bash
   # Install system dependencies (Ubuntu)
   sudo apt-get install python3-pip python3-dev python3-venv cmake ninja-build \
       autoconf flex bison ccache numactl build-essential

   # Build all components
   source setup.sh
   make build-all
   ```

4. **Verify Installation**
   ```bash
   python -c 'import assassyn'
   make test-all
   ```

### Development Workflow

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/<your-feature-name>
   ```

2. **Follow Code Guidelines** (from `.cursor/rules/write-good-code.mdc`):
   - Avoid unnecessary wrappers and indirections
   - Refactor repeated code into unified interfaces
   - Use `@dataclass` for Python structs
   - Annotate function signatures with types
   - Use `typing.TYPE_CHECKING` to prevent cyclic imports

3. **Read Relevant Documentation**
   - Architecture: `docs/design/arch/arch.md`
   - DSL Design: `docs/design/lang/dsl.md`
   - Build System: `docs/design/internal/build-system.md`
   - Tutorials: `tutorials/*.qmd` (Quarto markdown)

4. **Run Tests Before Committing**
   ```bash
   source setup.sh  # Required for pre-commit hooks
   make test-all    # Run all tests
   make pylint      # Python linting
   make rust-lint   # Rust formatting and clippy
   ```

5. **Commit with Meaningful Messages**
   Use tags in commit messages:
   - `[dsl]` - DSL/frontend changes
   - `[bugfix]` - Bug fixes
   - `[enhancement]` - Feature improvements
   - `[docs]` - Documentation updates
   - `[test]` - Test additions/modifications

   Example: `[dsl][enhancement]: Add support for multi-port arrays`

6. **Submit Pull Request**
   - Push to your fork: `git push origin feature/<your-feature-name>`
   - Create PR to `master` branch
   - Wait for CI checks and code review

### Resolving Conflicts
```bash
git remote add upstream https://github.com/synthesys-lab/assassyn
git fetch upstream
git rebase upstream/master
git push -f origin <your-dev-branch>
```

---

## Key Areas for Contribution

### 1. Core IR Extensions (`python/assassyn/ir/`)
- New data types in `dtype.py`
- New expression nodes in `expr/`
- Memory system enhancements in `memory/`

### 2. Code Generation Backends (`python/assassyn/codegen/`)
- **Simulator**: Rust code generation in `simulator/`
- **Verilog**: RTL generation via PyCDE in `verilog/`

### 3. Example Applications (`examples/`)
- CPU designs (minor-cpu, o3-cpu)
- Accelerators (systolic-array, fft, spmv)
- Algorithm implementations (merge-sort, radix-sort, kmp)

### 4. IP Blocks (`python/assassyn/ip/`)
- Reusable hardware components
- Credit-based flow control modules

### 5. Documentation (`docs/`, `tutorials/`)
- Design documents in `docs/design/`
- Tutorials in Quarto format (`*.qmd`)

---

## Testing Infrastructure

### Unit Tests (`python/unit-tests/`)
29 tests covering:
- Type enforcement
- Codegen metadata (FIFO, register files, arrays)
- Ramulator2 integration
- PyCDE wrapper functionality

### CI/Integration Tests (`python/ci-tests/`)
52 tests covering:
- Module functionality (arbiter, record, inline ops)
- Memory systems (SRAM, DRAM)
- Control flow primitives
- Credit system mechanics

### Running Tests
```bash
source setup.sh
pytest -n 8 python/unit-tests   # Unit tests (parallel)
pytest -n 8 python/ci-tests     # Integration tests (parallel)
```

---

## Container/VM Support

### Docker
```bash
docker build -t assassyn .
docker run -it assassyn
```

### Apptainer (HPC environments)
See `docs/vm/apptainer.md` for HPC cluster deployment.

---

## Summary

- ✅ **No proprietary dependencies** - All external code is from public repositories
- ✅ **Well-documented** - Comprehensive design docs and tutorials
- ✅ **Modular architecture** - Clear separation between IR, codegen, and tools
- ✅ **Dual-target generation** - Simulation and RTL from single source
- ✅ **Active CI/CD** - GitHub Actions for testing and validation

For questions or issues, submit to: https://github.com/synthesys-lab/assassyn/issues
