const state = {
  user: null,
  accounts: [],
  selectedAccountId: null,
};

const els = {
  status: document.querySelector("#api-status"),
  message: document.querySelector("#message"),
  loginTab: document.querySelector("#login-tab"),
  signupTab: document.querySelector("#signup-tab"),
  loginForm: document.querySelector("#login-form"),
  signupForm: document.querySelector("#signup-form"),
  demoButton: document.querySelector("#demo-button"),
  accountForm: document.querySelector("#account-form"),
  accountList: document.querySelector("#account-list"),
  postList: document.querySelector("#post-list"),
  sentimentBars: document.querySelector("#sentiment-bars"),
  metricAccounts: document.querySelector("#metric-accounts"),
  metricPosts: document.querySelector("#metric-posts"),
  metricEngagement: document.querySelector("#metric-engagement"),
  metricSentiment: document.querySelector("#metric-sentiment"),
};

async function api(path, options = {}) {
  const response = await fetch(`/api${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(body.error || body.message || `Erro ${response.status}`);
  }
  return body;
}

function setMessage(text, type = "info") {
  els.message.textContent = text;
  els.message.style.color = type === "error" ? "#b42318" : "#68736d";
}

function setAuthMode(mode) {
  const isLogin = mode === "login";
  els.loginTab.classList.toggle("active", isLogin);
  els.signupTab.classList.toggle("active", !isLogin);
  els.loginForm.classList.toggle("hidden", !isLogin);
  els.signupForm.classList.toggle("hidden", isLogin);
  setMessage("");
}

function formatPercent(value) {
  const number = Number(value || 0);
  return `${number.toFixed(1)}%`;
}

function sentimentLabel(breakdown) {
  if (!breakdown) return "-";
  const entries = Object.entries(breakdown);
  if (!entries.length) return "-";
  const [label] = entries.sort((a, b) => b[1] - a[1])[0];
  const labels = { positive: "Positivo", negative: "Negativo", neutral: "Neutro" };
  return labels[label] || "-";
}

function updateAccountList() {
  els.metricAccounts.textContent = state.accounts.length;

  if (!state.accounts.length) {
    els.accountList.innerHTML = '<div class="empty">Nenhuma conta monitorada</div>';
    return;
  }

  els.accountList.innerHTML = state.accounts.map((account) => `
    <div class="account-row">
      <div>
        <strong>@${account.username}</strong>
        <div class="post-meta">
          <span>${account.followers_count || 0} seguidores</span>
          <span>${account.posts_count || 0} posts</span>
        </div>
      </div>
      <button type="button" data-account-id="${account.id}">Abrir</button>
    </div>
  `).join("");

  els.accountList.querySelectorAll("button[data-account-id]").forEach((button) => {
    button.addEventListener("click", () => loadDashboard(Number(button.dataset.accountId)));
  });
}

function renderSentimentBars(breakdown) {
  const labels = [
    ["positive", "Positivo", "positive"],
    ["neutral", "Neutro", "neutral"],
    ["negative", "Negativo", "negative"],
  ];
  const total = Object.values(breakdown || {}).reduce((sum, value) => sum + Number(value || 0), 0) || 1;

  els.sentimentBars.innerHTML = labels.map(([key, label, className]) => {
    const value = Number((breakdown || {})[key] || 0);
    const width = Math.round((value / total) * 100);
    return `
      <div class="bar-row">
        <span>${label}</span>
        <div class="bar-track"><div class="bar-fill ${className}" style="width: ${width}%"></div></div>
        <span>${value}</span>
      </div>
    `;
  }).join("");
}

function renderPosts(posts) {
  els.metricPosts.textContent = posts.length;

  if (!posts.length) {
    els.postList.innerHTML = '<div class="empty">Nenhum post encontrado</div>';
    return;
  }

  els.postList.innerHTML = posts.map((post) => `
    <div class="post-row">
      <strong>${post.caption || "Post sem legenda"}</strong>
      <div class="post-meta">
        <span>${post.likes_count || 0} curtidas</span>
        <span>${post.comments_count || 0} comentarios</span>
        <span>${formatPercent(post.engagement_rate)}</span>
        <span>${post.sentiment_label || "sem analise"}</span>
      </div>
    </div>
  `).join("");
}

async function loadAccounts() {
  if (!state.user) return;
  const data = await api(`/accounts?user_id=${state.user.id}`);
  state.accounts = data.accounts || [];
  updateAccountList();
}

async function loadDashboard(accountId) {
  state.selectedAccountId = accountId;
  const [analytics, posts] = await Promise.all([
    api(`/accounts/${accountId}/analytics`),
    api(`/accounts/${accountId}/posts?limit=10`),
  ]);

  els.metricEngagement.textContent = formatPercent(analytics.average_engagement);
  els.metricSentiment.textContent = sentimentLabel(analytics.sentiment_breakdown);
  renderSentimentBars(analytics.sentiment_breakdown || {});
  renderPosts(posts.posts || []);
}

async function login(email, password) {
  const data = await api("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  state.user = data.user;
  setMessage(`Logado como ${state.user.username}.`);
  await loadAccounts();
  if (state.accounts[0]) await loadDashboard(state.accounts[0].id);
}

els.loginTab.addEventListener("click", () => setAuthMode("login"));
els.signupTab.addEventListener("click", () => setAuthMode("signup"));

els.loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    await login(
      document.querySelector("#login-email").value,
      document.querySelector("#login-password").value,
    );
  } catch (error) {
    setMessage(error.message, "error");
  }
});

els.signupForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    const payload = {
      full_name: document.querySelector("#signup-name").value,
      username: document.querySelector("#signup-username").value,
      email: document.querySelector("#signup-email").value,
      password: document.querySelector("#signup-password").value,
    };
    await api("/auth/signup", { method: "POST", body: JSON.stringify(payload) });
    setAuthMode("login");
    document.querySelector("#login-email").value = payload.email;
    setMessage("Conta criada.");
  } catch (error) {
    setMessage(error.message, "error");
  }
});

els.accountForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!state.user) {
    setMessage("Entre antes de adicionar contas.", "error");
    return;
  }

  try {
    const username = document.querySelector("#account-username").value;
    const data = await api("/accounts", {
      method: "POST",
      body: JSON.stringify({ user_id: state.user.id, instagram_username: username }),
    });
    document.querySelector("#account-username").value = "";
    await loadAccounts();
    await loadDashboard(data.account_id);
  } catch (error) {
    setMessage(error.message, "error");
  }
});

els.demoButton.addEventListener("click", async () => {
  try {
    await api("/demo/seed", { method: "POST", body: JSON.stringify({}) });
    document.querySelector("#login-email").value = "demo@sensus.local";
    document.querySelector("#login-password").value = "demo123";
    await login("demo@sensus.local", "demo123");
  } catch (error) {
    setMessage(error.message, "error");
  }
});

async function checkHealth() {
  try {
    await api("/health");
    els.status.textContent = "Online";
    els.status.classList.add("ok");
  } catch (error) {
    els.status.textContent = "Offline";
    els.status.classList.add("error");
  }
}

checkHealth();
