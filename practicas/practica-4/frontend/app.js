const API_URL = "http://localhost:8000/chat";
const PROFILES_URL = "http://localhost:8000/profiles";

const form = document.getElementById("chatForm");
const chat = document.getElementById("chat");
const metricsGrid = document.getElementById("metricsGrid");
const profileInfo = document.getElementById("profileInfo");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");
const loadProfileBtn = document.getElementById("loadProfileBtn");

const messageInput = document.getElementById("message");
const systemPromptInput = document.getElementById("system_prompt");
const profileSelect = document.getElementById("copilot_profile");

let conversationId = null;
let profiles = {};

async function loadProfiles() {
  try {
    const response = await fetch(PROFILES_URL);

    if (!response.ok) {
      throw new Error("No se pudo consultar el endpoint /profiles.");
    }

    profiles = await response.json();
    loadSelectedProfile();

  } catch (error) {
    console.error("No se pudieron cargar los perfiles:", error);
    systemPromptInput.value =
      "No se pudieron cargar los perfiles desde el backend. Verifica que FastAPI esté ejecutándose en http://localhost:8000.";
  }
}

function loadSelectedProfile() {
  const profileId = profileSelect.value;

  if (profiles[profileId]) {
    systemPromptInput.value = profiles[profileId].system_prompt;
  }
}

function getConfig() {
  return {
    model: document.getElementById("model").value,
    copilot_profile: profileSelect.value,
    system_prompt: systemPromptInput.value,
    temperature: Number(document.getElementById("temperature").value),
    top_p: Number(document.getElementById("top_p").value),
    num_predict: Number(document.getElementById("num_predict").value),
    num_ctx: Number(document.getElementById("num_ctx").value),
    repeat_penalty: Number(document.getElementById("repeat_penalty").value)
  };
}

function addMessage(role, content, type = "assistant") {
  const div = document.createElement("div");
  div.className = `message ${type}`;
  div.innerHTML = `<strong>${escapeHtml(role)}</strong>${escapeHtml(content)}`;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function renderMetrics(data) {
  const metrics = data.metrics;

  profileInfo.innerHTML = `
    <strong>Perfil usado:</strong> ${escapeHtml(data.copilot_label)}
    <br>
    <strong>Modelo:</strong> ${escapeHtml(data.model)}
  `;

  const items = [
    ["Tiempo backend", `${metrics.wall_time_s.toFixed(3)} s`],
    ["Tiempo Ollama", `${metrics.total_duration_s.toFixed(3)} s`],
    ["Carga modelo", `${metrics.load_duration_s.toFixed(3)} s`],
    ["Tokens entrada", metrics.prompt_eval_count],
    ["Tokens salida", metrics.eval_count],
    ["Tokens totales", metrics.total_tokens],
    ["Generación", `${metrics.eval_duration_s.toFixed(3)} s`],
    ["Tokens/s", metrics.tokens_per_second.toFixed(2)]
  ];

  metricsGrid.innerHTML = items
    .map(([label, value]) => `
      <div class="metric-card">
        <small>${label}</small>
        <strong>${value}</strong>
      </div>
    `)
    .join("");
}

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const message = messageInput.value.trim();

  if (!message) {
    return;
  }

  const payload = {
    message,
    conversation_id: conversationId,
    ...getConfig()
  };

  addMessage("Usuario", message, "user");
  messageInput.value = "";
  sendBtn.disabled = true;
  sendBtn.textContent = "Generando...";

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Error desconocido");
    }

    conversationId = data.conversation_id;
    addMessage(`Copiloto (${data.copilot_label})`, data.reply, "assistant");
    renderMetrics(data);

  } catch (error) {
    addMessage("Error", error.message, "error");

  } finally {
    sendBtn.disabled = false;
    sendBtn.textContent = "Enviar";
  }
});

clearBtn.addEventListener("click", () => {
  conversationId = null;
  chat.innerHTML = "";
  profileInfo.textContent = "Sin perfil usado todavía";
  metricsGrid.innerHTML = "<span>Sin datos todavía</span>";
});

loadProfileBtn.addEventListener("click", loadSelectedProfile);
profileSelect.addEventListener("change", loadSelectedProfile);

loadProfiles();
