import logging
from typing import Generator, Any, Dict, List

from prospectiva.interfaces.stt import TextGenerator

logger = logging.getLogger(__name__)


class FallbackLLM(TextGenerator):
    """
    Wrapper que intenta con el LLM primario; si falla, cae al secundario.
    """
    def __init__(self, primary: TextGenerator, secondary: TextGenerator):
        self.primary = primary
        self.secondary = secondary

    def generate(self, prompt: str, system_prompt: str | None = None) -> Generator[str, None, None]:
        yield from self.primary.generate(prompt, system_prompt)

    def generate_with_tools(self, prompt: str, tools: List[Dict[str, Any]],
                          system_prompt: str | None = None) -> Dict[str, Any]:
        result = self.primary.generate_with_tools(prompt, tools, system_prompt)
        # Solo caer al secundario si finish_reason=error (fracaso real)
        # No caer en finish_reason=stop (respuesta valida aunque sin tools)
        if result.get("finish_reason") == "error":
            logger.warning("[FallbackLLM] Primary failed, falling back to secondary")
            return self.secondary.generate_with_tools(prompt, tools, system_prompt)
        return result

    def send_tool_results(self, tool_calls: List[Dict], tool_results: List[Dict],
                         system_prompt: str | None = None) -> Dict[str, Any]:
        return self.primary.send_tool_results(tool_calls, tool_results, system_prompt)

    def stream_tool_results(self, tool_calls: List[Dict], tool_results: List[Dict],
                           system_prompt: str | None = None):
        collected = []
        try:
            for chunk in self.primary.stream_tool_results(tool_calls, tool_results, system_prompt):
                collected.append(chunk)
                yield chunk
        except Exception:
            logger.warning("[FallbackLLM] Primary stream failed, using secondary")
            resp = self.secondary.send_tool_results(tool_calls, tool_results, system_prompt)
            text = resp.get("content", "") or ""
            if text:
                yield text
            yield None
