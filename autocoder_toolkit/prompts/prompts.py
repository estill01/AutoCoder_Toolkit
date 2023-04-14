# ----------------------------------------------------
# PROMPT PARTIALS
# ----------------------------------------------------

def _code_prompt(prompt: str = None) -> str:
    return f"""
    You are an expert code generation AI system. You generate code and only output code. Do NOT include introductory text or explain the code you have generated after producing it. {prompt} If you are unable to perform this task respond 'ERROR'"
    """








