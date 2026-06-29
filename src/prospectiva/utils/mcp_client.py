import os
import json
import logging
import time
from typing import Any, Dict, List, Optional
import httpx

logger = logging.getLogger(__name__)


class MCPError(Exception):
    pass


class MCPClient:
    """
    MCP JSON-RPC client for the external campus information server.

    Connects to a FastMCP server (e.g. mcp-blu) via JSON-RPC 2.0 over HTTP.
    Follows the MCP protocol: initialize -> initialized -> call tools.
    """

    def __init__(self, url: str | None = None, token: str | None = None, timeout: float = 10.0):
        self.url = (url or os.getenv("MCP_URL", "http://localhost:8000/mcp")).rstrip("/")
        self.token = token or os.getenv("MCP_BEARER_TOKEN", "")
        self.timeout = timeout
        self._req_id = 0
        self._available = False
        self._initialized = False
        self._server_info: dict = {}
        self._client = httpx.Client(timeout=timeout)
        self._connect()

    def _headers(self) -> dict:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _send(self, method: str, params: dict | None = None) -> dict:
        self._req_id += 1
        body = {
            "jsonrpc": "2.0",
            "id": self._req_id,
            "method": method,
            "params": params or {},
        }
        try:
            resp = self._client.post(self.url, json=body, headers=self._headers())
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                logger.error("[MCPClient] Authentication failed (401) - check MCP_BEARER_TOKEN")
            elif e.response.status_code == 404:
                logger.error(f"[MCPClient] MCP endpoint not found at {self.url}")
            else:
                logger.error(f"[MCPClient] HTTP {e.response.status_code}: {e.response.text[:200]}")
            raise MCPError(f"HTTP {e.response.status_code}") from e
        except httpx.ConnectError as e:
            logger.error(f"[MCPClient] Connection refused at {self.url}")
            raise MCPError(f"Connection refused: {e}") from e
        except httpx.TimeoutException as e:
            logger.error(f"[MCPClient] Timeout at {self.url}")
            raise MCPError(f"Timeout: {e}") from e
        except Exception as e:
            logger.error(f"[MCPClient] Request error: {e}")
            raise MCPError(str(e)) from e

        if "error" in data:
            err = data["error"]
            msg = f"MCP error {err.get('code', '?')}: {err.get('message', '?')}"
            logger.error(f"[MCPClient] {msg}")
            if "data" in err:
                logger.error(f"  detail: {err['data']}")
            raise MCPError(msg)

        return data.get("result", {})

    def _connect(self):
        """Initialize MCP connection: initialize + initialized notification."""
        try:
            # Step 1: Initialize
            init_result = self._send("initialize", {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "campus-assistant", "version": "1.0"},
            })
            self._server_info = init_result.get("serverInfo", {})
            protocol = init_result.get("protocolVersion", "?")
            logger.info(f"[MCPClient] Connected to {self._server_info.get('name', '?')} "
                        f"v{self._server_info.get('version', '?')} (protocol {protocol})")

            # Step 2: Send initialized notification
            self._client.post(self.url, json={
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
                "params": {},
            }, headers=self._headers())

            self._available = True
            self._initialized = True

        except MCPError:
            logger.warning(f"[MCPClient] MCP server not available at {self.url}")
            self._available = False
        except Exception as e:
            logger.warning(f"[MCPClient] Connection failed: {e}")
            self._available = False

    def _call_tool(self, name: str, arguments: dict | None = None) -> Any:
        """Call a tool on the MCP server."""
        if not self._available:
            return {"error": "MCP server not available"}
        try:
            result = self._send("tools/call", {
                "name": name,
                "arguments": arguments or {},
            })
            # FastMCP con json_response=True expone el resultado tipado en
            # structuredContent.result; el bloque 'content' puede perder la
            # estructura de listas en algunas versiones. Preferimos el
            # structuredContent cuando existe.
            structured = result.get("structuredContent")
            if isinstance(structured, dict) and "result" in structured:
                return structured["result"]

            content = result.get("content", [])
            for block in content:
                if block.get("type") == "text":
                    text = block.get("text", "")
                    try:
                        return json.loads(text)
                    except json.JSONDecodeError:
                        return {"result": text}
            return content if content else result
        except MCPError as e:
            return {"error": str(e)}

    def is_available(self) -> bool:
        return self._available

    # ──────────────────────────────────────────────
    # Server tool methods
    # ──────────────────────────────────────────────

    def health_check(self) -> dict:
        return self._call_tool("health_check")

    def database_summary(self) -> dict:
        return self._call_tool("database_summary")

    def list_places(self, place_type: str | None = None) -> list[dict]:
        return self._call_tool("list_places", {"place_type": place_type} if place_type else {})

    def search_places(self, query: str) -> list[dict]:
        return self._call_tool("search_places", {"query": query})

    def get_place_detail(self, place_id: str) -> dict:
        return self._call_tool("get_place_detail", {"place_id": place_id})

    def get_place_detail_by_name(self, name: str) -> dict:
        return self._call_tool("get_place_detail_by_name", {"name": name})

    def get_restaurant_menu(self, place_id: str) -> dict:
        return self._call_tool("get_restaurant_menu", {"place_id": place_id})

    def get_restaurant_menu_by_name(self, name: str) -> dict:
        return self._call_tool("get_restaurant_menu_by_name", {"name": name})

    def search_food(self, query: str, max_price: float | None = None) -> list[dict]:
        args: dict = {"query": query}
        if max_price is not None:
            args["max_price"] = max_price
        return self._call_tool("search_food", args)

    def get_store_products(self, place_id: str) -> list[dict]:
        return self._call_tool("get_store_products", {"place_id": place_id})

    def search_products(self, query: str, max_price: float | None = None) -> list[dict]:
        args: dict = {"query": query}
        if max_price is not None:
            args["max_price"] = max_price
        return self._call_tool("search_products", args)

    def find_office_by_need(self, query: str) -> list[dict]:
        return self._call_tool("find_office_by_need", {"query": query})

    def get_gates(self) -> list[dict]:
        return self._call_tool("get_gates")

    def search_semantic_documents(self, query: str) -> list[dict]:
        return self._call_tool("search_semantic_documents", {"query": query})

    def get_current_crowd_levels(self) -> list[dict]:
        return self._call_tool("get_current_crowd_levels")

    def __del__(self):
        try:
            self._client.close()
        except Exception:
            pass