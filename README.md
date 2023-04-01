# Code Translation Toolkit 🪄
This toolkit helps you translate code between different programming languages, find alternative imports for packages, and perform various code processing tasks such as error fixing, refactoring, and removing extraneous text.

## Requirements
- Python 3.6+
- `openai` library

## Installation
1. Install the `openai` library using pip:
```bash
pip install openai
```

2. Clone or download the repository to your local machine.

## Usage
### Importing the Toolkit
To use the toolkit, simply import the necessary functions from the `code_translation_toolkit.py` file:

```python
from code_translation_toolkit import translate_code, find_imports, is_external_import, find_alternative_imports
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

### Optional: Batch API Calls
To optimize API calls and minimize the number of requests, you can use the optional prompt batching feature. Import the necessary functions from the `code_translation_toolkit.py` file:

```python
from code_translation_toolkit import create_batched_prompt, batch_api_call, extract_responses
```

Create a list of tasks, then use the `create_batched_prompt`, `batch_api_call`, and `extract_responses` functions to batch the API calls:

```python
tasks = [...]  # List of tasks
prompt = create_batched_prompt(tasks)
response_text = batch_api_call(prompt)
responses = extract_responses(response_text)
```

Refer to the refactored code in the previous response for examples of how to use the batching feature with the available functions.

## Contributing
Contributions are welcome! If you have suggestions for improvements or bug fixes, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
