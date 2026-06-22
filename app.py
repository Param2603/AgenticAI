"""
app.py  —  Param Shah's Digital Twin
Streamlit UI: chat interface with RAG + tools
Run: streamlit run app.py
"""

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Param Shah | Digital Twin",
    page_icon="🧑‍💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

  html, body, [class*="css"] {
      font-family: 'Space Grotesk', sans-serif;
  }

  /* ══════════════════════════════════════
     BACKGROUND
  ══════════════════════════════════════ */
  .stApp {
      background: linear-gradient(135deg, #0f0c29 0%, #1a0533 40%, #0c1445 100%);
      color: #f0e6ff;
  }

  /* ══════════════════════════════════════
     SIDEBAR
  ══════════════════════════════════════ */
  [data-testid="stSidebar"] {
      background: linear-gradient(180deg, #0f0c29 0%, #1a0533 100%);
      border-right: 1px solid rgba(168, 85, 247, 0.4);
  }
  [data-testid="stSidebar"] * {
      color: #e9d5ff !important;
  }
  [data-testid="stSidebar"] .stButton > button {
      background: rgba(168, 85, 247, 0.12) !important;
      border: 1px solid rgba(168, 85, 247, 0.4) !important;
      color: #d8b4fe !important;
      border-radius: 8px !important;
      font-size: 0.78rem !important;
      transition: all 0.2s ease !important;
  }
  [data-testid="stSidebar"] .stButton > button:hover {
      background: rgba(168, 85, 247, 0.3) !important;
      border-color: #a855f7 !important;
      color: #ffffff !important;
      transform: translateX(4px) !important;
  }
  [data-testid="stSidebar"] input {
      background: rgba(168, 85, 247, 0.12) !important;
      border: 1px solid rgba(168, 85, 247, 0.4) !important;
      border-radius: 8px !important;
      color: #f0e6ff !important;
  }

  /* ══════════════════════════════════════
     CHAT MESSAGES — ASSISTANT
  ══════════════════════════════════════ */
  [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]),
  [data-testid="stChatMessage"]:nth-child(odd) {
      background: linear-gradient(135deg, rgba(88,28,135,0.45), rgba(30,27,75,0.6)) !important;
      border: 1px solid rgba(192, 132, 252, 0.35) !important;
      border-radius: 16px !important;
      margin-bottom: 12px !important;
      padding: 10px 14px !important;
      box-shadow: 0 4px 20px rgba(139, 92, 246, 0.15) !important;
  }

  /* ══════════════════════════════════════
     CHAT MESSAGES — USER
  ══════════════════════════════════════ */
  [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]),
  [data-testid="stChatMessage"]:nth-child(even) {
      background: linear-gradient(135deg, rgba(6,78,59,0.4), rgba(4,47,46,0.55)) !important;
      border: 1px solid rgba(52, 211, 153, 0.35) !important;
      border-radius: 16px !important;
      margin-bottom: 12px !important;
      padding: 10px 14px !important;
      box-shadow: 0 4px 20px rgba(16, 185, 129, 0.1) !important;
  }

  /* ══════════════════════════════════════
     ALL CHAT TEXT — BRIGHT & READABLE
  ══════════════════════════════════════ */
  [data-testid="stChatMessage"] p,
  [data-testid="stChatMessage"] span,
  [data-testid="stChatMessage"] div,
  [data-testid="stChatMessage"] li,
  [data-testid="stChatMessage"] strong {
      color: #f5f0ff !important;
      font-size: 0.97rem !important;
      line-height: 1.7 !important;
  }
  [data-testid="stChatMessage"] strong {
      color: #e9d5ff !important;
      font-weight: 700 !important;
  }

  /* ══════════════════════════════════════
     CHAT INPUT BAR — FIX WHITE BAR
  ══════════════════════════════════════ */
  [data-testid="stBottom"],
  [data-testid="stBottom"] > div,
  .stChatInputContainer,
  .stChatInputContainer > div {
      background: linear-gradient(135deg, #0f0c29, #1a0533) !important;
      border-top: 1px solid rgba(168, 85, 247, 0.3) !important;
  }
  .stChatInputContainer textarea,
  [data-testid="stChatInputTextArea"] {
      background: rgba(88, 28, 135, 0.25) !important;
      border: 1px solid rgba(168, 85, 247, 0.5) !important;
      border-radius: 14px !important;
      color: #f0e6ff !important;
      font-size: 0.97rem !important;
      caret-color: #c084fc !important;
  }
  .stChatInputContainer textarea::placeholder {
      color: #9f7aea !important;
      opacity: 0.8 !important;
  }
  .stChatInputContainer textarea:focus {
      border-color: #a855f7 !important;
      box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.25) !important;
      outline: none !important;
  }
  /* Send button */
  [data-testid="stChatInputSubmitButton"] button {
      background: linear-gradient(135deg, #7c3aed, #06b6d4) !important;
      border: none !important;
      border-radius: 10px !important;
      color: white !important;
  }
  [data-testid="stChatInputSubmitButton"] button:hover {
      background: linear-gradient(135deg, #6d28d9, #0891b2) !important;
      transform: scale(1.05) !important;
  }

  /* ══════════════════════════════════════
     HEADINGS
  ══════════════════════════════════════ */
  h1 {
      background: linear-gradient(135deg, #c084fc 0%, #67e8f9 50%, #c084fc 100%);
      background-size: 200%;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      font-weight: 700 !important;
      animation: shimmer 4s linear infinite;
  }
  @keyframes shimmer {
      0% { background-position: 0%; }
      100% { background-position: 200%; }
  }
  h2, h3 {
      color: #c084fc !important;
      font-weight: 600 !important;
  }

  /* ══════════════════════════════════════
     GENERAL TEXT
  ══════════════════════════════════════ */
  p, span, li, label {
      color: #e9d5ff !important;
  }

  /* ══════════════════════════════════════
     METRIC CARDS
  ══════════════════════════════════════ */
  [data-testid="metric-container"] {
      background: linear-gradient(135deg, rgba(88,28,135,0.3), rgba(6,78,59,0.2)) !important;
      border: 1px solid rgba(168, 85, 247, 0.4) !important;
      border-radius: 12px !important;
      padding: 10px !important;
  }
  [data-testid="metric-container"] label {
      color: #c084fc !important;
      font-size: 0.75rem !important;
  }
  [data-testid="metric-container"] [data-testid="stMetricValue"] {
      color: #67e8f9 !important;
      font-size: 0.95rem !important;
      font-weight: 700 !important;
  }

  /* ══════════════════════════════════════
     LAUNCH BUTTON
  ══════════════════════════════════════ */
  .stButton > button[kind="primary"] {
      background: linear-gradient(135deg, #7c3aed 0%, #0891b2 100%) !important;
      border: none !important;
      color: #ffffff !important;
      font-weight: 700 !important;
      border-radius: 12px !important;
      font-size: 1rem !important;
      padding: 0.7rem 1.5rem !important;
      box-shadow: 0 4px 25px rgba(124, 58, 237, 0.5) !important;
      transition: all 0.3s ease !important;
  }
  .stButton > button[kind="primary"]:hover {
      transform: translateY(-3px) !important;
      box-shadow: 0 8px 35px rgba(124, 58, 237, 0.7) !important;
  }

  /* ══════════════════════════════════════
     BADGES
  ══════════════════════════════════════ */
  .skill-badge {
      display: inline-block;
      background: linear-gradient(135deg, rgba(124,58,237,0.25), rgba(139,92,246,0.15));
      border: 1px solid rgba(192, 132, 252, 0.5);
      color: #e9d5ff;
      padding: 3px 11px;
      border-radius: 20px;
      font-size: 0.72rem;
      margin: 2px;
      font-family: 'JetBrains Mono', monospace;
  }
  .tool-badge {
      display: inline-block;
      background: linear-gradient(135deg, rgba(6,182,212,0.2), rgba(16,185,129,0.15));
      border: 1px solid rgba(52, 211, 153, 0.45);
      color: #6ee7b7;
      padding: 3px 11px;
      border-radius: 20px;
      font-size: 0.72rem;
      margin: 2px;
      font-family: 'JetBrains Mono', monospace;
  }

  /* ══════════════════════════════════════
     NAME CARD
  ══════════════════════════════════════ */
  .name-card {
      background: linear-gradient(135deg, rgba(88,28,135,0.35), rgba(6,78,59,0.25));
      border: 1px solid rgba(192, 132, 252, 0.45);
      border-radius: 14px;
      padding: 14px 16px;
      margin-bottom: 10px;
      text-align: center;
  }
  .name-card h2 {
      margin: 0 !important;
      font-size: 1.2rem !important;
      background: linear-gradient(135deg, #c084fc, #34d399);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
  }
  .name-card p {
      margin: 4px 0 0 0 !important;
      color: #a78bfa !important;
      font-size: 0.78rem !important;
  }

  /* ══════════════════════════════════════
     GLOW BAR & DIVIDER
  ══════════════════════════════════════ */
  .glow-bar {
      height: 2px;
      background: linear-gradient(90deg, transparent, #a855f7, #22d3ee, #a855f7, transparent);
      border-radius: 2px;
      margin: 6px 0 14px 0;
      animation: glow-pulse 3s ease-in-out infinite;
  }
  @keyframes glow-pulse {
      0%, 100% { opacity: 0.5; }
      50% { opacity: 1; }
  }
  hr {
      border: none !important;
      border-top: 1px solid rgba(168, 85, 247, 0.25) !important;
      margin: 12px 0 !important;
  }

  /* ══════════════════════════════════════
     STATUS DOT
  ══════════════════════════════════════ */
  .status-dot {
      width: 8px; height: 8px;
      background: #34d399;
      border-radius: 50%;
      display: inline-block;
      margin-right: 6px;
      box-shadow: 0 0 8px #34d399;
      animation: pulse 2s infinite;
  }
  @keyframes pulse {
      0%, 100% { box-shadow: 0 0 8px #34d399; }
      50% { box-shadow: 0 0 2px #34d399; opacity: 0.6; }
  }

  /* ══════════════════════════════════════
     SUBTITLE & WARNING
  ══════════════════════════════════════ */
  .subtitle {
      color: #c4b5fd !important;
      font-size: 1rem;
      margin-top: -6px;
  }
  .stAlert {
      background: rgba(88, 28, 135, 0.2) !important;
      border: 1px solid rgba(168, 85, 247, 0.4) !important;
      border-radius: 10px !important;
      color: #e9d5ff !important;
  }

  /* ══════════════════════════════════════
     SCROLLBAR
  ══════════════════════════════════════ */
  ::-webkit-scrollbar { width: 5px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: rgba(168, 85, 247, 0.5); border-radius: 10px; }
  ::-webkit-scrollbar-thumb:hover { background: #a855f7; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="name-card">
        <h2>🧑‍💻 Param Shah</h2>
        <p>Full Stack Developer · GTU CE Student</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="status-dot"></span> **Digital Twin Active**', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 🔑 API Keys")
    groq_key = st.text_input(
        "Groq API Key",
        value=os.getenv("GROQ_API_KEY", ""),
        type="password",
        placeholder="gsk_...",
        help="Get free key at console.groq.com",
    )
    gemini_key = st.text_input(
        "Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        placeholder="AIza...",
        help="Get free key at aistudio.google.com",
    )

    st.markdown("---")

    st.markdown("### 🛠️ Available Tools")
    st.markdown("""
    <span class="tool-badge">🧮 Calculator</span>
    <span class="tool-badge">🌐 Web Search</span>
    <span class="tool-badge">🕐 Date & Time</span>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### ⚡ Tech Stack")
    skills = ["React.js", "Node.js", "Express.js", "MongoDB", "JavaScript", "Tailwind CSS", "JWT", "REST APIs"]
    badges = "".join(f'<span class="skill-badge">{s}</span>' for s in skills)
    st.markdown(badges, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 💡 Try asking:")
    example_qs = [
        "Tell me about yourself",
        "What projects have you built?",
        "What are your strongest skills?",
        "Calculate 15% of 85000",
        "What's today's date?",
        "Search for latest React.js news",
        "Why should I hire you?",
    ]
    for q in example_qs:
        if st.button(q, use_container_width=True, key=f"ex_{q}"):
            st.session_state.pending_input = q

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        '<div style="font-size:0.7rem; color:#7c3aed; text-align:center; line-height:1.7;">'
        'Built with LangChain · Groq · Gemini · ChromaDB<br>'
        '<span style="color:#a78bfa;">© 2024 Param Shah Digital Twin</span>'
        '</div>',
        unsafe_allow_html=True,
    )


# ── Main header ────────────────────────────────────────────────────────────────
col_title, col_meta = st.columns([3, 1])
with col_title:
    st.markdown("# 🤖 Param Shah — Digital Twin")
    st.markdown('<div class="glow-bar"></div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">An AI version of Param that talks like him, knows his resume, and can use tools. '
        'Ask anything — from his skills to live web searches!</p>',
        unsafe_allow_html=True,
    )
with col_meta:
    st.markdown("&nbsp;")
    st.metric("🧠 LLM", "LLaMA-3.3-70B")
    st.metric("📦 Embeddings", "Gemini-001")
    st.metric("🗄️ VectorDB", "ChromaDB")

st.markdown("---")


# ── Session state init ─────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_ready" not in st.session_state:
    st.session_state.agent_ready = False
if "agent_fn" not in st.session_state:
    st.session_state.agent_fn = None
if "pending_input" not in st.session_state:
    st.session_state.pending_input = None


# ── Agent initialization ───────────────────────────────────────────────────────
def initialize_agent(groq_api_key: str, gemini_api_key: str):
    from rag_setup import get_or_build_vector_store
    from agent import build_agent

    with st.spinner("🔨 Building RAG knowledge base from resume..."):
        vector_store = get_or_build_vector_store(gemini_api_key)
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    with st.spinner("🤖 Initializing Param's Digital Twin..."):
        agent_fn = build_agent(groq_api_key, retriever)

    st.session_state.agent_fn = agent_fn
    st.session_state.agent_ready = True

    welcome = (
        "Hey! 👋 I'm **Param Shah** — well, the AI version of me! "
        "I'm a Full Stack Developer currently pursuing my B.E. in Computer Engineering at GTU. "
        "Ask me anything about my skills, projects, or background — or give me a task like "
        "searching the web, doing math, or checking the time. Let's chat!"
    )
    st.session_state.messages.append({"role": "assistant", "content": welcome})


# ── Init button ────────────────────────────────────────────────────────────────
if not st.session_state.agent_ready:
    if groq_key and gemini_key:
        if st.button("🚀 Launch Digital Twin", type="primary", use_container_width=True):
            initialize_agent(groq_key, gemini_key)
            st.rerun()
    else:
        st.warning("👈 Please enter your **Groq** and **Gemini** API keys in the sidebar to get started.")


# ── Chat display ───────────────────────────────────────────────────────────────
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        avatar = "🧑‍💻" if role == "assistant" else "🧑"
        with st.chat_message(role, avatar=avatar):
            st.markdown(content)


# ── Chat input ─────────────────────────────────────────────────────────────────
if st.session_state.agent_ready:
    prefill = st.session_state.get("pending_input")
    if prefill:
        st.session_state.pending_input = None
        user_input = prefill
    else:
        user_input = st.chat_input("Ask Param anything... 💬")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="🧑‍💻"):
            with st.spinner("Param is thinking... 🤔"):
                try:
                    response = st.session_state.agent_fn(
                        user_input,
                        st.session_state.chat_history,
                    )
                except Exception as e:
                    response = f"⚠️ Something went wrong: {e}\n\nPlease check your API keys and try again."
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()
else:
    if not (groq_key and gemini_key):
        pass