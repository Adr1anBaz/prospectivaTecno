import json
import sys
from typing import Any
from urllib.request import Request, urlopen
from urllib.error import URLError


class MCPClient:
    def __init__(self, url: str, token: str):
        self.url = url.rstrip("/")
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        }
        self._req_id = 0

    def _send(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        self._req_id += 1
        body = json.dumps({
            "jsonrpc": "2.0",
            "id": self._req_id,
            "method": method,
            "params": params or {},
        }).encode()
        req = Request(self.url, data=body, headers=self.headers, method="POST")
        try:
            with urlopen(req) as resp:
                data = json.loads(resp.read().decode())
        except URLError as e:
            print(f"[ERROR] HTTP {e.code if hasattr(e, 'code') else '??'}: {e.reason if hasattr(e, 'reason') else e}")
            sys.exit(1)

        if "error" in data:
            err = data["error"]
            print(f"[ERROR] {err.get('code', '?')}: {err.get('message', '?')}")
            if "data" in err:
                print(f"  detail: {err['data']}")
            sys.exit(1)

        return data.get("result", {})

    def initialize(self) -> dict:
        return self._send("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "campus-client", "version": "1.0"},
        })

    def initialized(self):
        req = Request(
            self.url,
            data=json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}).encode(),
            headers=self.headers,
            method="POST",
        )
        with urlopen(req):
            pass

    def ping(self) -> dict:
        return self._send("ping")

    def list_tools(self) -> list[dict]:
        result = self._send("tools/list")
        return result.get("tools", [])

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> Any:
        result = self._send("tools/call", {
            "name": name,
            "arguments": arguments or {},
        })
        content = result.get("content", [])
        for block in content:
            if block.get("type") == "text":
                return json.loads(block["text"])
        return content


def main():
    import os
    from dotenv import load_dotenv
    from pathlib import Path

    load_dotenv(Path(__file__).parent / ".env")

    token = os.getenv("MCP_BEARER_TOKEN")
    if not token:
        print("ERROR: MCP_BEARER_TOKEN not set in .env")
        sys.exit(1)

    url = os.getenv("MCP_URL", "http://localhost:8000/mcp")
    client = MCPClient(url, token)

    # 1. Initialize
    print(">>> initialize")
    init_result = client.initialize()
    print(f"    server: {init_result.get('serverInfo', {}).get('name', '?')} "
          f"v{init_result.get('serverInfo', {}).get('version', '?')}")
    print(f"    protocol: {init_result.get('protocolVersion', '?')}")
    print(f"    tools available: {len(init_result.get('capabilities', {}).get('tools', {}))}")

    # 2. Notify initialized (required by MCP protocol)
    print(">>> notifications/initialized")
    client.initialized()
    print("    done")

    # 3. Ping
    print(">>> ping")
    print(f"    {client.ping()}")

    # 4. List tools
    print(">>> tools/list")
    tools = client.list_tools()
    print(f"    {len(tools)} tools:")
    for t in tools:
        print(f"      - {t['name']}: {t.get('description', '?')}")

    # 5. Call a tool (health_check)
    print(">>> tools/call (health_check)")
    result = client.call_tool("health_check")
    print(f"    {json.dumps(result, indent=2)}")

    # 6. Call database_summary
    print(">>> tools/call (database_summary)")
    result = client.call_tool("database_summary")
    print(f"    {json.dumps(result, indent=2)}")


if __name__ == "__main__":
    main()

