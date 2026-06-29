#!/usr/bin/env bash
# ============================================================
# start.sh - Levanta servidores + asistente en una sola terminal
# ============================================================
# Ejecuta: bash start.sh
# - Postgres (docker), MCP server, Route server → background
# - Asistente (modo texto) → foreground (tu terminal)
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BLU_DIR="$SCRIPT_DIR/../mcp-blu"
LOG_DIR="/tmp/prospectiva-logs"
mkdir -p "$LOG_DIR"

# ── Validar API keys ──
source "$SCRIPT_DIR/.env" 2>/dev/null || true
if echo "$GROQ_API_KEY" | grep -qi "dummy\|your_\|sk-xxx"; then
  echo "⚠️  GROQ_API_KEY no configurada en .env"
  echo "   Edita $SCRIPT_DIR/.env con tu API key real"
  echo ""
fi
if echo "$DEEPGRAM_API_KEY" | grep -qi "dummy\|your_\|xxx"; then
  echo "⚠️  DEEPGRAM_API_KEY no configurada en .env"
  echo "   Edita $SCRIPT_DIR/.env con tu API key real"
  echo ""
fi

echo "============================================================"
echo " Iniciando infraestructura..."
echo "============================================================"

# ── 1. PostgreSQL ──
echo "[1/4] PostgreSQL..."
cd "$BLU_DIR"
if docker ps --format '{{.Names}}' 2>/dev/null | grep -q campus_postgres; then
  echo "  ya corriendo"
else
  docker compose up -d
  sleep 3
  echo "  ok"
fi

# ── 2. MCP server ──
echo "[2/4] MCP server (:8000)..."
cd "$BLU_DIR/mcp-server"
if ss -tlnp 2>/dev/null | grep -q ":8000 "; then
  echo "  ya corriendo"
else
  nohup uv run server.py > "$LOG_DIR/mcp.log" 2>&1 &
  echo "  PID $!"
fi

# ── 3. Route server ──
echo "[3/4] Route server (:8001)..."
cd "$BLU_DIR"
if ss -tlnp 2>/dev/null | grep -q ":8001 "; then
  echo "  ya corriendo"
else
  nohup uv run route_server.py > "$LOG_DIR/route.log" 2>&1 &
  echo "  PID $!"
fi

# ── Leer token de los .env ──
MCP_TOKEN=$(grep -E "^MCP_BEARER_TOKEN=" "$BLU_DIR/mcp-server/.env" 2>/dev/null | cut -d= -f2-)
if [ -z "$MCP_TOKEN" ]; then
  MCP_TOKEN=$(grep -E "^MCP_BEARER_TOKEN=" "$BLU_DIR/.env" 2>/dev/null | cut -d= -f2-)
fi

# ── 4. Esperar que respondan ──
echo ""
echo "Esperando servidores..."
for i in $(seq 1 15); do
  MCP_OK=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8000/mcp \
    -H "Content-Type: application/json" -H "Accept: application/json" \
    -H "Authorization: Bearer $MCP_TOKEN" \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' 2>/dev/null || echo "000")
  ROUTE_OK=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/api/health 2>/dev/null || echo "000")
  if [ "$MCP_OK" = "200" ] && [ "$ROUTE_OK" = "200" ]; then
    echo "  ✅ MCP y Route listos"
    break
  fi
  sleep 1
done

if [ "$MCP_OK" != "200" ]; then echo "  ⚠️ MCP no responde (log: $LOG_DIR/mcp.log)"; fi
if [ "$ROUTE_OK" != "200" ]; then echo "  ⚠️ Route no responde (log: $LOG_DIR/route.log)"; fi

# ── 5. Asistente ──
echo ""
echo "============================================================"
echo " Iniciando asistente (modo texto)..."
echo " Escribe tus comandos debajo."
echo " /exit para salir."
echo "============================================================"
echo ""

cd "$SCRIPT_DIR"
uv run python src/prospectiva/main.py --text

# ── Al salir ──
echo ""
echo "Asistente terminado. Los servidores siguen corriendo."
echo "Detenerlos con:  pkill -f 'uv run server.py' ; pkill -f 'uv run route_server.py'"
