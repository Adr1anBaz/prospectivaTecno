const API_URL = "http://localhost:8000/chat";
const CONVERSATIONS_URL = "http://localhost:8000/conversations";
const PROFILES_URL = "http://localhost:8000/profiles";

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
const statusProfileName = document.getElementById("statusProfileName");
const profileStatusBar = document.getElementById("profileStatusBar");

// Current conversation ID
let currentConversationId = null;

// Profiles cache
let profiles = {};

// Profile icons
const profileIcons = {
  "generico": "🤖",
  "docente": "👨‍🏫",
  "robotica": "🤖",
  "programacion": "💻",
  "investigacion": "📚"
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

function loadSelectedProfile() {
  const profileId = profileSelect.value;

  if (profiles[profileId]) {
    systemPromptInput.value = profiles[profileId].system_prompt;
    updateProfileIndicators(profiles[profileId].label, profileId);
  }
}

function updateProfileIndicators(profileLabel, profileId = null) {
  // Get profile ID if not provided
  if (!profileId) {
    profileId = profileSelect.value;
  }

  const icon = profileIcons[profileId] || "🤖";

  // Update badge in controls panel
  if (activeProfileName) {
    activeProfileName.textContent = profileLabel;
  }

  // Update badge icon
  const badgeIcon = document.querySelector('.badge-icon');
  if (badgeIcon) {
    badgeIcon.textContent = icon;
  }

  // Update status bar
  if (statusProfileName) {
    statusProfileName.textContent = profileLabel;
  }

  // Update status icon
  const statusIcon = document.querySelector('.status-icon');
  if (statusIcon) {
    statusIcon.textContent = icon;
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
  div.innerHTML = `<strong>${role}</strong>${escapeHtml(content)}`;
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

async function typeMessage(element, text, speed = 20) {
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
    ["Perfil usado", data.copilot_label],
    ["Modelo", data.model],
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

  // Show the floating button
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
  if (profileStatusBar) {
    profileStatusBar.style.display = 'block';
  }
}

function showWelcomeHeader() {
  welcomeHeader.classList.remove('hidden');
  if (profileStatusBar) {
    profileStatusBar.style.display = 'none';
  }
}

function escapeHtml(text) {
  return text
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

    // Display all messages
    data.messages.forEach(msg => {
      if (msg.role === "user") {
        addMessage("Usuario", msg.content, "user");
      } else if (msg.role === "assistant") {
        addMessage(`Modelo`, msg.content, "assistant");
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

  // Show thinking indicator
  addThinkingIndicator();

  try {
    console.log("Sending request to:", API_URL);
    console.log("Payload:", payload);

    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    console.log("Response status:", response.status);

    const data = await response.json();
    console.log("Response data:", data);

    if (!response.ok) {
      throw new Error(data.detail || "Error desconocido");
    }

    // Remove thinking indicator
    removeThinkingIndicator();

    // Update current conversation ID
    currentConversationId = data.conversation_id;

    // Add message with typing effect
    const messageObj = addMessageWithTyping(`${data.copilot_label}`, data.reply, "assistant");
    await messageObj.typeText();

    // Update profile indicators with the actual profile used
    updateProfileIndicators(data.copilot_label, data.copilot_profile);

    renderMetrics(data);

    // Save to localStorage
    localStorage.setItem("currentConversationId", currentConversationId);

  } catch (error) {
    console.error("Fetch error details:", error);
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

// Metrics modal
if (metricsToggleBtn) {
  metricsToggleBtn.addEventListener("click", openMetricsModal);
}

if (metricsCloseBtn) {
  metricsCloseBtn.addEventListener("click", closeMetricsModal);
}

// Close modal when clicking outside
if (metricsModal) {
  metricsModal.addEventListener("click", (e) => {
    if (e.target === metricsModal) {
      closeMetricsModal();
    }
  });
}

// Close modal with Escape key
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && metricsModal && metricsModal.classList.contains('open')) {
    closeMetricsModal();
  }
});

// On page load, try to restore the last conversation and load profiles
window.addEventListener("DOMContentLoaded", () => {
  // Load profiles first
  loadProfiles();

  // Then restore conversation if exists
  const savedConversationId = localStorage.getItem("currentConversationId");
  if (savedConversationId) {
    loadConversation(parseInt(savedConversationId));
  }
});
