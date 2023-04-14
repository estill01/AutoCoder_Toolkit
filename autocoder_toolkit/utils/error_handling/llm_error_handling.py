from autocoder_toolkit.utils import generate_task


def _handle_retries(response: str, max_attempts: int = 4):
    if response == "ERROR":
        pass
        """
        -> ask the LLM what the problem was : `diagnosis_error_response()`
        - parse the response
        - modify input and resubmit

        # retry up to max_tries 

        attempt = 0
       
        """

    else:
        return response

"""
def attempt_task_with_diagnosis(task: str, action: str, user_input: str, extra_info: str = "", temp: int = 0, max_attempts: int = 3) -> str:
    for attempt in range(max_attempts):
        response = generate_task(task, action, user_input, extra_info, temp)
        
        if response != "ERROR":
            return response
        
        diagnosis = diagnose_error_response(f"{task}: {action} {extra_info}", temp)
        if "suggestion:" in diagnosis.lower():
            suggestion = diagnosis.split("suggestion:", 1)[-1].strip()
            action = f"{action} {suggestion}"
        else:
            break

    return "ERROR: Unable to complete the task after multiple attempts and diagnosis."
"""


def diagnose_error_response(full_prompt: str, temp: int = 0) -> str:
    return generate_task(
        task="error diagnosis",
        action="Diagnose the reason for the 'ERROR' response in the following prompt and suggest how the prompt can be changed for a successful response:",
        user_input=full_prompt,
        temp=temp
    )

def request_clarification(full_prompt: str, temp: int = 0) -> str:
    return generate_task(
        task="clarification request",
        action="Identify any ambiguous or unclear parts in the following prompt and ask for clarification:",
        user_input=full_prompt,
        temp=temp
    )

def verify_input(input_data: str, validation_type: str, temp: int = 0) -> str:
    return generate_task(
        task="input verification",
        action=f"Verify the input data for {validation_type} issues and suggest corrections if needed:",
        user_input=input_data,
        temp=temp
    )

def try_simpler_task(original_task: str, fallback_tasks: List[str], user_input: str, extra_info: str = "", temp: int = 0) -> str:
    for fallback_task in fallback_tasks:
        response = generate_task(fallback_task, user_input, extra_info, temp)
        if response != "ERROR":
            return response
    # .. or just raise an Exception here (?)
    return "ERROR: Unable to complete the task with simpler alternatives."

