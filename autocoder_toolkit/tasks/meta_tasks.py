from typing import List
from autocoder_toolkit.utils import generate_task


# ========================
# META-TASKS
# ========================

# TODO -> `analyze` (?)
def analyze_code(code: str, analysis_type: str, temp: int = 0) -> List[str]:
    analysis_output = generate_task(
        task=f"{analysis_type} analysis",
        action=f"Analyze the following code and identify {analysis_type}:",
        user_input=code,
        temp=temp
    )
    return split_recommendations(analysis_output)


# TODO -> `make` (?)
def make_plan(item: str, plan_type: str, temp: int = 0) -> str:
    return generate_task(
        task=f"{plan_type} planning",
        action=f"Create a plan to address the following {plan_type}:",
        user_input=item,
        temp=temp
    )

# TODO -> `implement` (?)
def implement_task(code: str, task: str, temp: int = 0) -> str:
    return generate_task(
        task="task implementation",
        action="Implement the following task on the code:",
        user_input=code,
        extra_info=task,
        temp=temp
    )

def implement_plan(code: str, plans: List[str], temp: int = 0) -> str:
    updated_code = code
    for plan in plans:
        updated_code = implement_task(updated_code, plan, temp)
    return updated_code

def generate_code(component_type: str, requirements: str, temp: int = 0) -> str:
    return generate_task(
        task=f"{component_type} generation",
        action=f"Generate {component_type} code based on the following requirements:",
        user_input=requirements,
        temp=temp
    )


# --------


# TODO Increase abstraction on this
def compare_code(code1: str, code2: str, comparison_type: str, temp: int = 0) -> str:
    return generate_task(
        task=f"{comparison_type} comparison",
        action=f"Compare the following two code snippets based on {comparison_type}:",
        user_input=f"Code 1:\n{code1}\n\nCode 2:\n{code2}",
        temp=temp
    )

# TODO Increase abstraction?
def evaluate_technology(technology: str, evaluation_criteria: str, temp: int = 0) -> str:
    return generate_task(
        task=f"{technology} evaluation",
        action=f"Evaluate the following technology based on the given criteria:",
        user_input=evaluation_criteria,
        extra_info=technology,
        temp=temp
    )

# TODO Increase abstraction?
def transform_code(code: str, transformation_type: str, temp: int = 0) -> str:
    return generate_task(
        task=f"{transformation_type} transformation",
        action=f"Apply {transformation_type} transformation to the following code:",
        user_input=code,
        temp=temp
    )

# TODO Switch implementation to deterministic tech
def search_code(keyword: str, codebase: str, temp: int = 0) -> List[str]:
    search_results = generate_task(
        task="code search",
        action=f"Search the following codebase for occurrences of the keyword '{keyword}':",
        user_input=codebase,
        temp=temp
    )
    return split_recommendations(search_results)


