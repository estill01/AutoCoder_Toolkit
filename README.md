# AutoCoder Toolkit 🪄

The AutoCoder Toolkit helps you find and fix errors, perform code-quality refactoring, and translate code between different programming languages (while finding substitute packages and imports as it goes).

## Installation
Clone the repo then install the dependencies via `poetry`:
```bash
poetry install
```

## Usage
### Importing the Toolkit
Import the necessary functions from the module and get to toolkitting!:

```python
from auto_coder_toolkit import (
  refactor_code,
  update_code, 
  fix_errors, 
  translate_code, 
  find_imports, 
  is_external_import, 
  find_alternative_imports,
  process_directory,
 )
```

### Translating Code
Translate code from one language to another using the `translate_code` function:

```python
translated_code = translate_code(source_language, target_language, code)
```

- `source_language`: The source programming language (e.g., "Python")
- `target_language`: The target programming language (e.g., "JavaScript")
- `code`: The code to be translated

### Finding Import Statements
Find all import statements in a file using the `find_imports` function:

```python
import_statements = find_imports(file_path, source_language)
```

- `file_path`: The path to the file containing the code
- `source_language`: The source programming language (e.g., "Python")

### Determining if an Import Statement is External
Check if an import statement is for an external package or a reference to another file in the project using the `is_external_import` function:

```python
is_external = is_external_import(import_statement, source_language)
```
- `import_statement`: The import statement to check
- `source_language`: The source programming language (e.g., "Python")

### Finding Alternative Imports
Find alternative imports in the target language for a list of source language imports using the `find_alternative_imports` function:

```python
alternative_imports = find_alternative_imports(source_imports, source_language, target_language, browser_compatible=False)
```
- `source_imports`: A list of import statements in the source language
- `source_language`: The source programming language (e.g., "Python")
- `target_language`: The target programming language (e.g., "JavaScript")
- `browser_compatible` (optional): Set to `True` to find browser-compatible alternatives for JavaScript or TypeScript. Default is `False`.

## Contributing
Contributions are welcome! If you have suggestions for improvements or bug fixes, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
