from autocoder_toolkit import analyze_code, make_plan, implement_task


# ========================
# PIPELINES                 
# ========================

def refactor_and_optimize_code(code: str, analysis_type: str, plan_type: str, temp: int = 0) -> str:
    identified_items = analyze_code(code, analysis_type, temp)
    updated_code = code
    for item in identified_items:
        plan = make_plan(item, plan_type, temp)
        updated_code = implement_task(updated_code, plan, temp)
    return updated_code

