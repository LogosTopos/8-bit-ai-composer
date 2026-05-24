"""DeepSeek client for the isolated v3 8bc-ir-v1 composer."""

from __future__ import annotations

import json
import os
import re
from typing import Callable

from dotenv import load_dotenv
from openai import OpenAI

from .prompts import REPAIR_PROMPT, SYSTEM_PROMPT_B_FINAL

DEEPSEEK_BASE = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-v4-pro"
DEEPSEEK_FLASH_MODEL = "deepseek-v4-flash"

TokenCallback = Callable[[str, str], None]


class V3Composer:
    """Streaming client that asks the LLM for 8bc-ir-v1 JSON."""

    def __init__(self, model: str | None = None):
        load_dotenv()
        raw_model = model or os.getenv("DEEPSEEK_MODEL") or os.getenv("ANTHROPIC_MODEL") or DEEPSEEK_MODEL
        self.model = raw_model.split("[")[0].strip()
        self.client = OpenAI(
            api_key=os.getenv("CHAT_API_KEY", ""),
            base_url=os.getenv("DEEPSEEK_BASE", DEEPSEEK_BASE),
            timeout=300.0,
        )
        self.messages: list[dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT_B_FINAL}]
        self._last_raw = ""
        self._last_reasoning = ""

    def reset(self) -> None:
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT_B_FINAL}]
        self._last_raw = ""
        self._last_reasoning = ""

    def compose(self, prompt: str, on_token: TokenCallback | None = None) -> dict | None:
        self.messages.append({"role": "user", "content": prompt})
        return self._call(on_token=on_token)

    def refine(self, feedback: str, on_token: TokenCallback | None = None) -> dict | None:
        self.messages.append(
            {
                "role": "user",
                "content": (
                    "Revise the previous composition according to this feedback. "
                    "Return a complete replacement 8bc-ir-v1 JSON object only.\n\n"
                    f"Feedback: {feedback}"
                ),
            }
        )
        return self._call(on_token=on_token)

    def repair(self, issues: str, on_token: TokenCallback | None = None) -> dict | None:
        self.messages.append({"role": "user", "content": REPAIR_PROMPT.format(issues=issues)})
        return self._call(on_token=on_token)

    def _call(self, on_token: TokenCallback | None = None) -> dict | None:
        max_tokens = 65536 if "pro" in self.model.lower() else 24576
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=0.78,
                max_tokens=max_tokens,
                stream=True,
            )
        except Exception as exc:
            print(f"  [API Error] {exc}")
            return None

        content_parts: list[str] = []
        reasoning_parts: list[str] = []

        for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            reasoning = getattr(delta, "reasoning_content", "") or ""
            content = getattr(delta, "content", "") or ""

            if reasoning:
                reasoning_parts.append(reasoning)
                if on_token:
                    on_token(reasoning, "")
            if content:
                content_parts.append(content)
                if on_token:
                    on_token("", content)

        content = "".join(content_parts)
        reasoning = "".join(reasoning_parts)
        self._last_raw = content
        self._last_reasoning = reasoning

        parsed = self._extract_json(content)
        if parsed is not None:
            self.messages.append({"role": "assistant", "content": content})
            return parsed

        parsed = self._extract_json(reasoning)
        if parsed is not None:
            self.messages.append({"role": "assistant", "content": json.dumps(parsed, ensure_ascii=False)})
            return parsed

        return None

    @staticmethod
    def _extract_json(text: str) -> dict | None:
        text = (text or "").strip()
        if not text:
            return None

        try:
            value = json.loads(text)
            return value if isinstance(value, dict) else None
        except json.JSONDecodeError:
            pass

        block = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if block:
            try:
                value = json.loads(block.group(1).strip())
                return value if isinstance(value, dict) else None
            except json.JSONDecodeError:
                pass

        candidate = V3Composer._first_balanced_object(text)
        if candidate:
            try:
                value = json.loads(candidate)
                return value if isinstance(value, dict) else None
            except json.JSONDecodeError:
                return None
        return None

    @staticmethod
    def _first_balanced_object(text: str) -> str | None:
        start = text.find("{")
        if start < 0:
            return None

        depth = 0
        in_string = False
        escape = False
        for idx in range(start, len(text)):
            ch = text[idx]
            if in_string:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_string = False
                continue

            if ch == '"':
                in_string = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[start : idx + 1]
        return None

    @property
    def last_raw(self) -> str:
        return self._last_raw

    @property
    def last_reasoning(self) -> str:
        return self._last_reasoning

    @property
    def history_length(self) -> int:
        return len(self.messages)
