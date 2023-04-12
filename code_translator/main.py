import os
import openai
import dotenv
from typing import List
import tiktoken
from code_translator.utils import (
    num_tokens_from_messages, 
    build_prompt, 
    select_model,
    llm,
    MODELS
)


# TODO Add RAIL output formatters
# TODO Add streaming return variant


"""
Functions:

- `translate_code`

- `find_imports`

- `is_external_import`

- `find_alternative_imports`

- `process_directory`

- `update_code`

- `fix_errors`

- `execute_code`

- `refactor_code`

- `remove_extraneous_text`

"""



def translate_code(source_language, target_language, code, temp: int = 0):
    return llm(
        _code_prompt(f"Translate the following {source_language} code to {target_language} code."),
        code
    )

def find_imports(file_path, source_language):
    with open(file_path, "r") as f:
        code = f.read()

    content = llm(
        _code_prompt(f"Extract all import statements from the following {source_language} code. put each extracted import statement on a newline. Include the whole import statement including language syntax, imported files, classes, functions, and other code artifacts."),
        code
    )
    # TODO Use an output formatter to get a list of imports
    
    imports = content.split('\n')

    return [import_statement for import_statement in imports if import_statement.strip()]



## REFACTOR -- PICK BACK UP HERE  ##

def is_external_import(import_statement, source_language):
    prompt = f"Is the following {source_language} import statement an external package or a reference to another file in the project?\n\n{import_statement}\n\nAnswer:"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=50,
        temperature=0.7,
    )

    return response.choices[0].text.strip().lower() == "external"

def find_alternative_imports(source_imports, source_language, target_language, browser_compatible=False):
    alternative_imports = []

    for source_import in source_imports:
        prompt = f"Find a suitable {target_language} package that can replace the {source_language} package '{source_import}'."
        if browser_compatible and target_language.lower() in ['javascript', 'typescript']:
            prompt += " The {target_language} package should be compatible with running in a browser environment."
        prompt += f"\n\n{source_language} import statement:\n" + source_import

        response = openai.ChatCompletion.create(
            model="gpt-4",
            prompt=prompt,
            max_tokens=1024,
            temperature=0.7,
        )

        alternative_import = response.choices[0].text.strip()

        if not alternative_import:
            if browser_compatible and target_language.lower() in ['javascript', 'typescript']:
                raise ValueError(f"No browser-compatible {target_language} alternative found for the {source_language} import: {source_import}")
            else:
                raise ValueError(f"No {target_language} alternative found for the {source_language} import: {source_import}")

        alternative_imports.append(alternative_import)

    return alternative_imports

def process_directory(source_dir, output_dir, source_language, target_language, browser_compatible=False):
    source_extension = source_language.lower()[:2]  # Example: ".py" for Python
    target_extension = target_language.lower()[:2]  # Example: ".js" for JavaScript

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(f".{source_extension}"):
                file_path = os.path.join(root, file)
                output_file = os.path.join(output_dir, os.path.relpath(file_path, source_dir)).replace(f".{source_extension}", f".{target_extension}")

                os.makedirs(os.path.dirname(output_file), exist_ok=True)

                with open(file_path, "r") as f:
                    source_code = f.read()

                source_imports = find_imports(file_path, source_language)
                alternative_imports = find_alternative_imports(source_imports, source_language, target_language, browser_compatible)

                translated_code = translate_code(source_language, target_language, source_code)
                translated_code_with_imports = "\n".join(alternative_imports) + "\n\n" + translated_code
                with open(output_file, "w") as f:
                    f.write(translated_code_with_imports)



def update_code(code, error_message, target_language):
    prompt = f"Update the following {target_language} code to fix the error described:\n\nError message:\n{error_message}\n\n{target_language} code:\n{code}\n\nUpdated {target_language} code:"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.7,
    )

    return response.choices[0].text.strip()


def fix_errors(file_path, error_output, target_language):
    with open(file_path, "r") as f:
        code = f.read()

    fixed_code = update_code(code, error_output, target_language)

    with open(file_path, "w") as f:
        f.write(fixed_code)


def execute_code(file_path):
    # This function should be implemented based on the specific target language and execution environment
    pass


def refactor_code(file_path, target_language):
    with open(file_path, "r") as f:
        code = f.read()

    prompt = f"Refactor the following {target_language} code to ensure a high level of encapsulation and abstraction, as if implemented by an expert software engineer:\n\n{target_language} code:\n{code}\n\nRefactored {target_language} code:"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.7,
    )

    refactored_code = response.choices[0].text.strip()

    with open(file_path, "w") as f:
        f.write(refactored_code)

def remove_extraneous_text(file_path, target_language):
    with open(file_path, "r") as f:
        code = f.read()

    prompt = f"Remove any extraneous text from the following {target_language} code, leaving only code and relevant comments:\n\n{target_language} code:\n{code}\n\nCleaned {target_language} code:"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.7,
    )

    cleaned_code = response.choices[0].text.strip()

    with open(file_path, "w") as f:
        f.write(cleaned_code)




# TODO Improve implementation
if __name__ == "__main__":
    load_dotenv()

    source_dir = "source"
    output_dir = "output"
    source_language = "Python"
    target_language = "JavaScript"
    browser_compatible = True

    process_directory(source_dir, output_dir, source_language, target_language, browser_compatible)

    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".js"):
                file_path = os.path.join(root, file)

                try:
                    execute_code(file_path)
                except Exception as e:
                    error_output = str(e)
                    fix_errors(file_path, error_output, target_language)

                refactor_code(file_path, target_language)
                remove_extraneous_text(file_path, target_language)

    print("Done!")



# Example usage
# source_directory = "path/to/your/source/project"
# output_directory = "path/to/output/directory"
# source_language = "Python"  # Change this to another language if desired
# target_language = "JavaScript"  # Change this to another language if desired
#
# process_directory(source_directory, output_directory, source_language, target_language)

