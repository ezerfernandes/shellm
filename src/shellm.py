#!/usr/bin/env python3

"""Initial version of shellm."""
import json
import os
import sys

from dotenv import load_dotenv
import requests


load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    msg = "OPENROUTER_API_KEY must be set."
    raise ValueError(msg)

LLM_MODEL = os.getenv("LLM_MODEL", "mistralai/mixtral-8x7b-instruct")


def get_shell_command(question: str) -> str:
    """Get shell command from message."""
    content = (
        f'[INST]Provide only a shell command for: "{question}". '
        "Avoid providing additional text, only provide the shell command.[/INST]"
    )

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                "model": LLM_MODEL,
                "messages": [
                    {"role": "user", "content": content},
                ],
            }
        ),
    )

    response.raise_for_status()
    answer = response.json().get("choices", [{}])[0].get("message", {}).get("content")
    if not answer:
        msg = "No answer returned by LLM model."
        raise ValueError(msg)

    if answer.startswith("```bash"):
        answer = answer[7:]
    elif answer.startswith("```shell"):
        answer = answer[8:]
    elif answer.startswith("```"):
        answer = answer[3:]

    if answer.endswith("```"):
        answer = answer[:-3]

    return answer.strip()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        input_string = sys.argv[0]
    else:
        input_string = sys.argv[1]
    print(get_shell_command(input_string))
