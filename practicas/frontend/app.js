const API_URL = "http://localhost:8000/chat";
const CONVERSATIONS_URL = "http://localhost:8000/conversations";
const PROFILES_URL = "http://localhost:8000/profiles";
const PROVIDERS_URL = "http://localhost:8000/providers";

const form = document.getElementById("chatForm");
const chat = document.getElementById("chat");
const metricsGrid = document.getElementById("metricsGrid");
const metricsModal = document.getElementById("metricsModal");
const metricsToggleBtn = document.getElementById("metricsToggleBtn");
const metricsCloseBtn = document.getElementById("metricsCloseBtn");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");
const messageInput = document.getElementById("message");
const controlsPanel = document.getElementById("controlsPanel");
const toggleControlsBtn = document.getElementById("toggleControls");
const newConversationBtn = document.getElementById("newConversation");
const welcomeHeader = document.getElementById("welcomeHeader");

// Copilot profile elements
const profileSelect = document.getElementById("copilot_profile");
const systemPromptInput = document.getElementById("system_prompt");
const loadProfileBtn = document.getElementById("loadProfileBtn");
const activeProfileName = document.getElementById("activeProfileName");

// Provider elements
const providerSelect = document.getElementById("provider");
const modelSelect = document.getElementById("model");

// Status bar elements
const statusModelText = document.getElementById("statusModelText");
const statusProfileText = document.getElementById("statusProfileText");

// Current conversation ID
let currentConversationId = null;

// Profiles cache
let profiles = {};

// Fallback provider models (used if backend is not running)
let providerModels = {
  "ollama": ["llama3.2:3b", "gemma3:4b", "qwen2.5:7b", "mistral:7b"],
  "gemini": ["gemini-2.5-flash", "gemini-2.5-flash-lite"],
  "groq": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
  "openrouter": ["google/gemma-2-9b-it:free", "mistralai/mistral-7b-instruct:free", "meta-llama/llama-3.2-3b-instruct:free"],
};

// Profile icons
const profileIcons = {
  "generico": "🤖",
  "docente": "👨‍🏫",
  "robotica": "🤖",
  "programacion": "💻",
  "investigacion": "📚"
};

// Provider icons
const providerIcons = {
  "ollama": "🦙",
  "gemini": "✨",
  "groq": "⚡",
  "openrouter": "🌐"
};

// Load profiles from backend
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

// Load providers from backend
async function loadProviders() {
  try {
    const response = await fetch(PROVIDERS_URL);

    if (!response.ok) {
      throw new Error("No se pudo consultar el endpoint /providers.");
    }

    providerModels = await response.json();

  } catch (error) {
    console.error("Usando modelos por defecto (backend no disponible):", error);
  }

  renderModelOptions();
}

function renderModelOptions() {
  const provider = providerSelect.value;
  const models = providerModels[provider] || [];

  modelSelect.innerHTML = "";
  models.forEach((model) => {
    const opt = document.createElement("option");
    opt.value = model;
    opt.textContent = model;
    modelSelect.appendChild(opt);
  });

  updateStatusBar();
}

function updateStatusBar() {
  const provider = providerSelect.value;
  const model = modelSelect.value || "sin modelo";
  const icon = providerIcons[provider] || "⚡";

  if (statusModelText) {
    statusModelText.textContent = `${provider} / ${model}`;
  }

  const statusIcon = document.querySelector('.model-status-bar .status-icon');
  if (statusIcon) {
    statusIcon.textContent = icon;
  }

  if (statusProfileText) {
    const profileId = profileSelect.value;
    const profileLabel = profiles[profileId] ? profiles[profileId].label : profileSelect.options[profileSelect.selectedIndex].text;
    statusProfileText.textContent = profileLabel;
  }
}

function loadSelectedProfile() {
  const profileId = profileSelect.value;

  if (profiles[profileId]) {
    systemPromptInput.value = profiles[profileId].system_prompt;
    updateProfileIndicators(profiles[profileId].label, profileId);
  }

  updateStatusBar();
}

function updateProfileIndicators(profileLabel, profileId = null) {
  if (!profileId) {
    profileId = profileSelect.value;
  }

  const icon = profileIcons[profileId] || "🤖";

  if (activeProfileName) {
    activeProfileName.textContent = profileLabel;
  }

  const badgeIcon = document.querySelector('.badge-icon');
  if (badgeIcon) {
    badgeIcon.textContent = icon;
  }
}

// Auto-resize textarea
messageInput.addEventListener('input', function() {
  this.style.height = 'auto';
  this.style.height = Math.min(this.scrollHeight, 200) + 'px';
});

// Send message with Enter (Shift+Enter for new line)
messageInput.addEventListener('keydown', function(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    form.dispatchEvent(new Event('submit'));
  }
});

// Toggle controls panel
toggleControlsBtn.addEventListener('click', () => {
  controlsPanel.classList.toggle('open');
});

// New conversation
newConversationBtn.addEventListener('click', () => {
  clearConversation();
});

function getConfig() {
  return {
    provider: providerSelect.value,
    model: modelSelect.value,
    copilot_profile: profileSelect.value,
    system_prompt: systemPromptInput.value,
    temperature: Number(document.getElementById("temperature").value),
    top_p: Number(document.getElementById("top_p").value),
    max_tokens: Number(document.getElementById("max_tokens").value),
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
  return div;
}

function addThinkingIndicator() {
  const div = document.createElement("div");
  div.className = "message thinking";
  div.id = "thinking-indicator";
  div.innerHTML = `<strong>Modelo</strong><div class="typing-indicator"><span></span><span></span><span></span></div>`;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

function removeThinkingIndicator() {
  const indicator = document.getElementById("thinking-indicator");
  if (indicator) {
    indicator.remove();
  }
}

async function typeMessage(element, text, speed = 15) {
  const contentContainer = document.createElement("span");
  element.appendChild(contentContainer);

  for (let i = 0; i < text.length; i++) {
    contentContainer.textContent += text[i];
    chat.scrollTop = chat.scrollHeight;
    await new Promise(resolve => setTimeout(resolve, speed));
  }
}

function addMessageWithTyping(role, content, type = "assistant") {
  const div = document.createElement("div");
  div.className = `message ${type}`;
  const roleElement = document.createElement("strong");
  roleElement.textContent = role;
  div.appendChild(roleElement);
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return { element: div, typeText: () => typeMessage(div, content) };
}

function renderMetrics(data) {
  const metrics = data.metrics;

  const items = [
    ["Proveedor", data.provider],
    ["Modelo", data.model],
    ["Perfil usado", data.copilot_label],
    ["Tiempo backend", `${metrics.wall_time_s.toFixed(3)} s`],
    ["Tiempo proveedor", `${metrics.provider_duration_s.toFixed(3)} s`],
    ["Tokens entrada", metrics.prompt_tokens],
    ["Tokens salida", metrics.completion_tokens],
    ["Tokens totales", metrics.total_tokens],
    ["Tokens/s aprox.", metrics.tokens_per_second.toFixed(2)]
  ];

  metricsGrid.innerHTML = items
    .map(([label, value]) => `
      <div class="metric-card">
        <small>${label}</small>
        <strong>${value}</strong>
      </div>
    `)
    .join("");

  if (metricsToggleBtn) {
    metricsToggleBtn.style.display = "flex";
  }
}

function openMetricsModal() {
  if (metricsModal) {
    metricsModal.classList.add('open');
  }
}

function closeMetricsModal() {
  if (metricsModal) {
    metricsModal.classList.remove('open');
  }
}

function hideWelcomeHeader() {
  welcomeHeader.classList.add('hidden');
}

function showWelcomeHeader() {
  welcomeHeader.classList.remove('hidden');
}

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function clearConversation() {
  currentConversationId = null;
  localStorage.removeItem("currentConversationId");
  chat.innerHTML = "";
  metricsGrid.innerHTML = "";
  if (metricsToggleBtn) {
    metricsToggleBtn.style.display = "none";
  }
  closeMetricsModal();
  showWelcomeHeader();
  controlsPanel.classList.remove('open');
}

async function loadConversation(conversationId) {
  try {
    const response = await fetch(`${CONVERSATIONS_URL}/${conversationId}`);
    if (!response.ok) {
      throw new Error("No se pudo cargar la conversación");
    }

    const data = await response.json();
    chat.innerHTML = "";
    hideWelcomeHeader();

    data.messages.forEach(msg => {
      if (msg.role === "user") {
        addMessage("Usuario", msg.content, "user");
      } else if (msg.role === "assistant") {
        addMessage("Modelo", msg.content, "assistant");
      }
    });

    currentConversationId = conversationId;
  } catch (error) {
    console.error("Error loading conversation:", error);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const message = messageInput.value.trim();

  if (!message) {
    return;
  }

  const payload = {
    message,
    conversation_id: currentConversationId,
    ...getConfig()
  };

  hideWelcomeHeader();
  addMessage("Usuario", message, "user");
  messageInput.value = "";
  messageInput.style.height = 'auto';
  sendBtn.disabled = true;
  sendBtn.textContent = "Generando...";

  addThinkingIndicator();

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

    removeThinkingIndicator();

    currentConversationId = data.conversation_id;

    const roleLabel = `${data.copilot_label} (${data.provider} / ${data.model})`;
    const messageObj = addMessageWithTyping(roleLabel, data.reply, "assistant");
    await messageObj.typeText();

    updateProfileIndicators(data.copilot_label, data.copilot_profile);

    // Update status bar
    if (statusModelText) {
      statusModelText.textContent = `${data.provider} / ${data.model}`;
    }
    if (statusProfileText) {
      statusProfileText.textContent = data.copilot_label;
    }

    renderMetrics(data);

    localStorage.setItem("currentConversationId", currentConversationId);

  } catch (error) {
    removeThinkingIndicator();

    let errorMessage = error.message;
    if (error.message === "Failed to fetch") {
      errorMessage = "No se puede conectar al servidor. Verifica que:\n1. El backend esté corriendo en http://localhost:8000\n2. No haya problemas de CORS\n3. Tu navegador permita la conexión";
    }

    addMessage("Error", errorMessage, "error");

  } finally {
    sendBtn.disabled = false;
    sendBtn.textContent = "Enviar";
  }
});

clearBtn.addEventListener("click", () => {
  clearConversation();
});

// Profile management
loadProfileBtn.addEventListener("click", loadSelectedProfile);
profileSelect.addEventListener("change", loadSelectedProfile);

// Provider change updates model list
providerSelect.addEventListener("change", renderModelOptions);

// Model change updates status bar
modelSelect.addEventListener("change", updateStatusBar);

// Metrics modal
if (metricsToggleBtn) {
  metricsToggleBtn.addEventListener("click", openMetricsModal);
}

if (metricsCloseBtn) {
  metricsCloseBtn.addEventListener("click", closeMetricsModal);
}

if (metricsModal) {
  metricsModal.addEventListener("click", (e) => {
    if (e.target === metricsModal) {
      closeMetricsModal();
    }
  });
}

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && metricsModal && metricsModal.classList.contains('open')) {
    closeMetricsModal();
  }
});

// On page load
window.addEventListener("DOMContentLoaded", () => {
  // Render model options immediately from fallback data
  renderModelOptions();

  // Then load from backend (will update if available)
  loadProfiles();
  loadProviders();

  const savedConversationId = localStorage.getItem("currentConversationId");
  if (savedConversationId) {
    loadConversation(parseInt(savedConversationId));
  }
});
