import os
import openai
import tiktoken
from typing import List, Callable
from autocoder_toolking.utils.constants import MODELS
from autocoder_toolking.utils.error_handling import _handle_retries

# TODO Switch to dotenv 
openai.api_key = os.environ["OPENAI_API_KEY"]


# TODO Integrate logging

# ----------------------------------------------------
# PRIMARY INTERFACE
# ----------------------------------------------------

def generate_task(
    task: str, 
    action: str, 
    user_input: str = None, 
    extra_info: str = "", 
    temp: int = 0, 
    messages: List[Dict[str, str]] = []
) -> str:
    prompt = _generate_system_prompt(task, action, extra_info)
    return _handle_retries(llm(prompt, user_input, temp, messages))

def llm(system_instruction: str = None, user_input: str = None, temp: int = 0, messages: List[Dict[str, str]] = []) -> str:
    messages = build_prompt(
        system=system_instruction
        user=user_input,
        messages=messages
    )
    model = select_model(messages)
    response = openai.ChatCompletion.create(
        model=model
        messages=messages,
        temperature=temp,
        max_tokens=MODELS[model].max_tokens
    )
    return response.choices[0].message.content


# ----------------------------------------------------
# PROMPT PARTIAL
# ----------------------------------------------------

def _generate_system_prompt(task: str, action: str, extra_info: str = "") -> str:
    return f"""
    You are an expert {task} AI system. {action} {extra_info} If you are unable to perform this task respond 'ERROR'"
    """


# ----------------------------------------------------
# PROMPT CONSTRUCTION
# ----------------------------------------------------

# SOURCE: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

def select_model(messages: List[Dict[str, str]], model_family: str = 'gpt-4', force: bool = False) -> str:
    msg_count = len(messages)
    token_count = num_tokens_from_messages(messages, model_family)
    avg_tokens_message = int(token_count / msg_count)
    count = token_count + avg_tokens_message

    if model_family == MODELS['gpt-3.5-turbo'].model:
        if count < MODELS['gpt-3.5-turbo'].max_tokens or force:
            return MODELS['gpt-3.5-turbo'].model
        else:
            raise ValueError(f"{MODELS['gpt-3.5-turnbo'].model}: Token count ({count}) greater than max allowed tokens ({MODELS['gpt-3.5-turbo'].max_tokens}).")
    if count < MODELS['gpt-4'].max_tokens: 
        return MODELS['gpt-4'].model
    elif count < MODELS['gpt-4-32k'].max_tokens or force:
        return MODELS['gpt-4-32k'].model
    else:
        raise ValueError(f"{MODELS['gpt-4-32k'].model}: Token count ({count}) greater than max allowed tokens ({MODELS['gpt-4-32k'].max_tokens}).")

def _build_user_prompt(content: str) -> Dict[str, str]:
    return {'role': 'user', 'content': conent }

def _build_system_prompt(content: str) -> Dict[str, str]:
    return {'role': 'system', 'content': content }

def build_prompt(
    *, 
    system_content: str = None, 
    user_content: str = None, 
    messages: List[Dict[str, str]] = [], 
    ) -> List[Dict[str, str]]:

    if system_content is not None and user_content is not None:
        return messages.extend([_make_system_prompt(system_content), _make_user_prompt(user_content)])
    if system_content is None and user_content is not None:
        return messages.extend([_make_user_prompt(user_content)])
    else
        raise ValueError("Must provide `user_content`")

