import os
import time
import json
import logging
from typing import Generator, Any, Dict, List

from prospectiva.interfaces.stt import TextGenerator

logger = logging.getLogger(__name__)

class GroqLLM(TextGenerator):
    def __init__(self, api_key: str | None = None, model: str = "meta-llama/llama-4-scout-17b-16e-instruct", max_tokens: int = 160):
        from groq import Groq
        self.client = Groq(api_key=api_key or os.getenv("GROQ_API_KEY"))
        self.model = model
        self.max_tokens = max_tokens
        logger.info(f"[GroqLLM] Initialized with model={model}, max_tokens={max_tokens}")

    def generate(self, prompt: str, system_prompt: str | None = None) -> Generator[str, None, None]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            start = time.time()
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                max_tokens=self.max_tokens,
                temperature=0.1,
                timeout=30.0
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta
            elapsed = time.time() - start
            logger.info(f"[GroqLLM] Generation completed in {elapsed:.2f}s")
        except Exception as e:
            logger.error(f"[GroqLLM] Error: {e}")
            yield "Lo siento, no puedo responder en este momento."

    def generate_with_tools(self, prompt: str, tools: List[Dict[str, Any]], 
                          system_prompt: str | None = None) -> Dict[str, Any]:
        """
        Generate text with tool calling support.
        
        Returns dict with:
        - content: str (response text if no tools)
        - tool_calls: list of tool calls (if tools were called)
        - finish_reason: str (stop, tool_calls, etc.)
        - raw_response: the full response object
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            start = time.time()
            logger.info(f"[GroqLLM] Calling with {len(tools)} tools available")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                max_tokens=self.max_tokens,
                temperature=0.1,
                timeout=30.0
            )
            
            message = response.choices[0].message
            finish_reason = response.choices[0].finish_reason
            
            elapsed = time.time() - start
            logger.info(f"[GroqLLM] Tool call response in {elapsed:.2f}s, finish_reason={finish_reason}")
            
            result = {
                "content": message.content,
                "tool_calls": [],
                "finish_reason": finish_reason,
                "raw_response": response,
            }
            
            if message.tool_calls:
                for tc in message.tool_calls:
                    result["tool_calls"].append({
                        "id": tc.id,
                        "name": tc.function.name,
                        "arguments": json.loads(tc.function.arguments),
                        "type": tc.type,
                    })
                logger.info(f"[GroqLLM] Model called {len(result['tool_calls'])} tool(s): "
                          + ", ".join([t['name'] for t in result['tool_calls']]))
            
            return result
            
        except Exception as e:
            logger.error(f"[GroqLLM] Tool call error: {e}")
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
            if streaming:
                stream = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=self.max_tokens,
                    temperature=0.1,
                    timeout=30.0,
                    stream=True,
                )
                full_content = ""
                for chunk in stream:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        full_content += delta
                        yield delta
                yield None  # signal end
                logger.info(f"[GroqLLM] Streamed {len(full_content)} chars")
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=self.max_tokens,
                    temperature=0.1,
                    timeout=30.0,
                )
                message = response.choices[0].message
                return {
                    "content": message.content,
                    "tool_calls": [],
                    "finish_reason": response.choices[0].finish_reason,
                    "raw_response": response,
                }
        except Exception as e:
            logger.error(f"[GroqLLM] Error in tool results: {e}")
            if streaming:
                yield ""
            else:
                return {
                    "content": "Lo siento, hubo un error.",
                    "tool_calls": [],
                    "finish_reason": "error",
                    "raw_response": None,
                }
