from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


@dataclass
class Tool:
    name: str
    description: str
    parameters: Dict[str, Any]
    func: Callable[..., Any]


def tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    parameters: Optional[Dict[str, Any]] = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        fn._tool = Tool(
            name=name or fn.__name__,
            description=description or (fn.__doc__ or "").strip(),
            parameters=parameters
            or {
                "type": "object",
                "properties": {},
                "required": [],
            },
            func=fn,
        )
        return fn

    return decorator


def get_tool(fn: Callable[..., Any]) -> Tool:
    return fn._tool
