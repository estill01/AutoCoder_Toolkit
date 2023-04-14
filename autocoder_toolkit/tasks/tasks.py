from autocoder_toolkit.utils import generate_task


# TODO Refactor these to use the meta-tasks more / better
# TODO Re-intergreate the code translation features from ._refactor/_old.py ; i.e. stripping out import statements and finding alternatives
# TODO Integrate DB / Chroma

# ========================
# TASKS
# ========================

# ------------------------
# ENHANCE
# ------------------------

def review_code(code: str, temp: int = 0) -> str:
    return generate_task(
        task="code review",
        action="Review the following code and provide feedback and suggestions for improvement:",
        user_input=code,
        temp=temp
    )


# TODO Swap this to multiple calls
def update_code(code: str, recommendations: Union[str, List[str]], temp: int = 0) -> str:
    if isinstance(recommendations, list):
        recommendations = '\n'.join(recommendations)
    return generate_task(
        task="code update",
        action="Update or enhance the following code using the provided recommendations:",
        user_input=code,
        extra_info=recommendations,
        temp=temp
    )

# ------------------------
# REFACTOR
# ------------------------

def refactor_code(code: str, reason: str, temp: int = 0) -> str:
    return generate_task(
        task="code refactoring",
        action="Refactor the following code:",
        user_input=code,
        extra_info=f"to {reason}.",
        temp=temp
    )

# ------------------------
# TESTING
# ------------------------

def generate_unit_tests(code: str, language: str, temp: int = 0) -> str:
    return generate_task(
        task="unit test generation",
        action="Generate unit tests for the following code:",
        user_input=code,
        extra_info=f"in {language}.",
        temp=temp
    )

# ------------------------
# BUGS
# ------------------------
def identify_bugs(code: str, temp: int = 0) -> str:
    return generate_task(
        task="bug detection",
        action="Identify any bugs in the following code and suggest potential fixes:",
        user_input=code,
        temp=temp
    )

def explain_bug_fixes(bug_report: str, temp: int = 0) -> str:
    return generate_task(
        task="bug fix explanation",
        action="Explain how to fix the bugs identified in the following report:",
        user_input=bug_report,
        temp=temp
    )

def fix_bugs(code: str, bug_fix_explanation: str, temp: int = 0) -> str:
    return generate_task(
        task="bug fixing",
        action="Fix the bugs in the following code using the provided bug fix explanation:",
        user_input=code,
        extra_info=bug_fix_explanation,
        temp=temp
    )

# -> check work

# ------------------------
# IMPLEMENT
# ------------------------

def implement_feature(feature_description: str, language: str, temp: int = 0) -> str:
    return generate_task(
        task="feature implementation",
        action="Implement the feature described in the user input:",
        user_input=feature_description,
        extra_info=f"in {language} code.",
        temp=temp
    )


# ------------------------
# CORRECTNESS CHECK
# ------------------------


def check_syntax(code: str, language: str, temp: int = 0) -> str:
    return generate_task(
        task="syntax check",
        action="Check the syntax of the following code and point out any errors:",
        user_input=code,
        extra_info=f"in {language}.",
        temp=temp
    )


# ------------------------
# TRANSLATE
# ------------------------

def translate_code(code: str, source_language: str, target_language: str, temp: int = 0) -> str:
    return generate_task(
        task="code translation",
        action="Translate the following code:",
        user_input=code,
        extra_info=f"from {source_language} to {target_language}.",
        temp=temp
    )
