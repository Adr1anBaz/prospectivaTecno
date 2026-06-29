import os
import json
import time
import logging
from typing import Generator, Any, Dict, List

import httpx
from prospectiva.interfaces.stt import TextGenerator

logger = logging.getLogger(__name__)


class OpenRouterLLM(TextGenerator):
    def __init__(self, api_key: str | None = None, model: str = "qwen/qwen3.6-flash", max_tokens: int = 160):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY", "")
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = model
        self.max_tokens = max_tokens
        logger.info(f"[OpenRouterLLM] model={model}, max_tokens={max_tokens}")

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/Adr1anBaz/prospectivaTecno",
        }

    def generate(self, prompt: str, system_prompt: str | None = None) -> Generator[str, None, None]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            start = time.time()
            with httpx.Client(timeout=30.0) as client:
                resp = client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self._headers(),
                    json={
                        "model": self.model,
                        "messages": messages,
                        "stream": True,
                        "max_tokens": self.max_tokens,
                        "temperature": 0.1,
                    },
                )
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if not line or line.startswith(":") or line == "data: [DONE]":
                        continue
                    if line.startswith("data: "):
                        chunk = json.loads(line[6:])
                        delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                        if delta:
                            yield delta
            elapsed = time.time() - start
            logger.info(f"[OpenRouterLLM] Generation completed in {elapsed:.2f}s")
        except Exception as e:
            logger.error(f"[OpenRouterLLM] Error: {e}")
            yield "Lo siento, no puedo responder en este momento."

    def generate_with_tools(self, prompt: str, tools: List[Dict[str, Any]],
                          system_prompt: str | None = None) -> Dict[str, Any]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            start = time.time()
            logger.info(f"[OpenRouterLLM] Calling with {len(tools)} tools available")

            body = {
                "model": self.model,
                "messages": messages,
                "tools": tools,
                "tool_choice": "auto",
                "max_tokens": self.max_tokens,
                "temperature": 0.1,
            }

            with httpx.Client(timeout=30.0) as client:
                resp = client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self._headers(),
                    json=body,
                )
                resp.raise_for_status()
                data = resp.json()

            choice = data["choices"][0]
            message = choice["message"]
            finish_reason = choice.get("finish_reason", "stop")

            elapsed = time.time() - start
            logger.info(f"[OpenRouterLLM] Response in {elapsed:.2f}s, finish_reason={finish_reason}")

            result = {
                "content": message.get("content"),
                "tool_calls": [],
                "finish_reason": finish_reason,
                "raw_response": data,
            }

            if message.get("tool_calls"):
                for tc in message["tool_calls"]:
                    result["tool_calls"].append({
                        "id": tc["id"],
                        "name": tc["function"]["name"],
                        "arguments": json.loads(tc["function"]["arguments"]),
                        "type": tc["type"],
                    })
                logger.info(f"[OpenRouterLLM] Model called {len(result['tool_calls'])} tool(s): "
                          + ", ".join([t['name'] for t in result['tool_calls']]))

            return result

        except Exception as e:
            logger.error(f"[OpenRouterLLM] Tool call error: {e}")
            return {
                "content": "Lo siento, no puedo responder en este momento.",
                "tool_calls": [],
                "finish_reason": "error",
                "raw_response": None,
            }

    def send_tool_results(self, tool_calls: List[Dict], tool_results: List[Dict],
                         system_prompt: str | None = None) -> Dict[str, Any]:
        return self._stream_tool_results(tool_calls, tool_results, system_prompt)

    def stream_tool_results(self, tool_calls: List[Dict], tool_results: List[Dict],
                           system_prompt: str | None = None):
        return self._stream_tool_results(tool_calls, tool_results, system_prompt, streaming=True)

    def _stream_tool_results(self, tool_calls: List[Dict], tool_results: List[Dict],
                            system_prompt: str | None = None, streaming: bool = False):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": tc["id"],
                    "type": "function",
                    "function": {
                        "name": tc["name"],
                        "arguments": json.dumps(tc["arguments"]),
                    }
                }
                for tc in tool_calls
            ]
        })

        for result in tool_results:
            messages.append({
                "role": "tool",
                "tool_call_id": result["tool_call_id"],
                "content": json.dumps(result["result"]),
            })

        try:
            body = {
                "model": self.model,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "temperature": 0.1,
            }
            if streaming:
                body["stream"] = True

            with httpx.Client(timeout=30.0) as client:
                if streaming:
                    full_content = ""
                    with client.stream("POST", f"{self.base_url}/chat/completions", headers=self._headers(), json=body) as resp:
                        resp.raise_for_status()
                        for line in resp.iter_lines():
                            if not line or line == "data: [DONE]" or line.startswith(":") or not line.startswith("data: "):
                                continue
                            chunk = json.loads(line[6:])
                            delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if delta:
                                full_content += delta
                                yield delta
                    yield None
                    logger.info(f"[OpenRouterLLM] Streamed {len(full_content)} chars")
                else:
                    resp = client.post(f"{self.base_url}/chat/completions", headers=self._headers(), json=body)
                    resp.raise_for_status()
                    data = resp.json()
                    message = data["choices"][0]["message"]
                    return {
                        "content": message.get("content"),
                        "tool_calls": [],
                        "finish_reason": data["choices"][0].get("finish_reason", "stop"),
                        "raw_response": data,
                    }
        except Exception as e:
            logger.error(f"[OpenRouterLLM] Error: {e}")
            if streaming:
                yield ""
            else:
                return {"content": "Lo siento, hubo un error.", "tool_calls": [], "finish_reason": "error", "raw_response": None}
