---
id: ARCH-execution-guide
title: "Application Execution Guide"
type: documentation
layer: presentation
owner: @vibe-team
version: v1
status: current
created: 2025-06-08
updated: 2025-06-08
tags: [run, execution, cli, package]
depends_on: []
referenced_by: []
---
## Context
This guide explains the correct procedure for running the `vibe-python` application. Due to its structure as an installable Python package, it cannot be run by directly executing its `.py` files. Attempting to do so (e.g., `python src/vibe_python/main.py`) will result in an `ImportError: attempted relative import with no known parent package`.

This error occurs because relative imports (like `from .config import ...`) require the file to be loaded as part of a recognized package, which doesn't happen when a file is run as a top-level script.

## Structure
The project follows a standard `src` layout:
```
vibe-python/
├── pyproject.toml
└── src/
    └── vibe_python/
        ├── __init__.py
        └── main.py
```
The `pyproject.toml` defines a console script entry point, which is the preferred way to run the application.

## Behavior
There are two correct ways to run the application, both of which must be executed from the project's root directory (`vibe-python/`).

### Method 1: Installing the Package (Recommended)
This method installs the package in "editable" mode, meaning changes to the source code are immediately reflected without needing to reinstall. It also creates the `vibe-python` command in your environment's path.

1.  **Install the package:**
    ```bash
    pip install -e .
    ```
2.  **Run the application:**
    ```bash
    vibe-python --help
    vibe-python list-robots
    ```

### Method 2: Running as a Module (For Development)
This method tells Python to run the `vibe_python.main` module from within the package context, which correctly resolves relative imports. This is useful for quick tests without installation.

1. **Run the module:**
   ```bash
   python -m vibe_python.main list-robots
   ```

## Evolution
### Historical
*   **v1:** Created in response to bug report `bugs/001.md` to clarify the correct execution procedure. 