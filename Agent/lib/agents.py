from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List, Optional

from openai import OpenAI

from lib.tooling import Tool


class Agent:
    def __init__(
        self,
        model: str,
        tools: Iterable[Tool],
        system_prompt: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        self.model = model
        self.tools = list(tools)
        self.system_prompt = system_prompt or ""
        self.client = OpenAI(api_key=api_key)

    def _tool_defs(self) -> List[Dict[str, Any]]:
        defs: List[Dict[str, Any]] = []
        for tool in self.tools:
            defs.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                    },
                }
            )
        return defs

    def _tool_map(self) -> Dict[str, Tool]:
        return {tool.name: tool for tool in self.tools}

    def run(self, user_query: str, max_steps: int = 6) -> Dict[str, Any]:
        messages: List[Dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": user_query})

        tool_defs = self._tool_defs()
        tool_map = self._tool_map()

        for _ in range(max_steps):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tool_defs,
                tool_choice="auto",
            )
            message = response.choices[0].message
            if message.tool_calls:
                messages.append(
                    {
                        "role": "assistant",
                        "content": message.content or "",
                        "tool_calls": [tc.model_dump() for tc in message.tool_calls],
                    }
                )
                for tool_call in message.tool_calls:
                    name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments or "{}")
                    tool = tool_map.get(name)
                    if not tool:
                        result = {"error": f"Tool not found: {name}"}
                    else:
                        result = tool.func(**args)
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(result, ensure_ascii=False),
                        }
                    )
                continue

            return {
                "answer": message.content or "",
                "messages": messages,
            }

        return {
            "answer": "Reached max steps without a final response.",
            "messages": messages,
        }
