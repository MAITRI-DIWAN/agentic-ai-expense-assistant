from ollama import chat

from assistant.tools import (
    get_total_expenses,
    get_category_total,
    get_highest_spending_category,
)


MODEL_NAME = "qwen2.5:3b"

MAX_TOOL_ROUNDS = 5

AVAILABLE_TOOLS = {
    "get_total_expenses": get_total_expenses,
    "get_category_total": get_category_total,
    "get_highest_spending_category": get_highest_spending_category,
}


SYSTEM_PROMPT = """
You are an AI Expense Assistant.

Your responsibilities:
1. Answer questions about recorded expenses.
2. Use the provided tools to retrieve expense information.
3. Never invent expense amounts.
4. Do not claim a calculation was performed unless a tool returned it.
5. If a category has no recorded expenses, explain that clearly.
6. Keep responses concise and easy to understand.
7. Do not modify or delete any expense records.
"""


def run_agent(user_message: str) -> str:
    """
    Run the local LLM agent and execute approved read-only tools.
    """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]

    for _ in range(MAX_TOOL_ROUNDS):

        response = chat(
            model=MODEL_NAME,
            messages=messages,
            tools=[
                get_total_expenses,
                get_category_total,
                get_highest_spending_category,
            ],
        )

        assistant_message = response.message

        # Save the model's response to the conversation.
        messages.append(assistant_message)

        tool_calls = assistant_message.tool_calls or []

        # If no tool is requested, return the final answer.
        if not tool_calls:
            return assistant_message.content or (
                "The model returned an empty response."
            )

        # Execute each requested tool.
        for tool_call in tool_calls:

            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            # Never execute a function that isn't allowlisted.
            tool_function = AVAILABLE_TOOLS.get(tool_name)

            if tool_function is None:
                tool_result = "Error: Requested tool is not available."

            else:
                try:
                    tool_result = tool_function(**arguments)

                except Exception:
                    # Log the actual exception on the server.
                    # Do not expose internal details to the model.
                    tool_result = (
                        "The requested operation failed. "
                        "Please try again."
                    )

            messages.append(
                {
                    "role": "tool",
                    "name": tool_name,
                    "content": str(tool_result),
                }
            )

    return (
        "I could not complete the request within the allowed "
        "number of tool-calling rounds."
    )