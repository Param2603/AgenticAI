"""
app.py  —  Param Shah's Digital Twin
Streamlit UI: chat interface with RAG + tools
Run: streamlit run app.py
"""

import os
import streamlit as st
from dotenv import load_dotenv

# ── Load .env ────────────────────────────────
load_dotenv()

# ── Page config (MUST be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="Param Shah | Digital Twin",
    page_icon="🧑‍💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

  html, body, [class*="css"] {
      font-family: 'Space Grotesk', sans-serif;
  }

  /* Dark premium background */
  .stApp {
      background: linear-gradient(135deg, #0a0a0f 0%, #111827 50%, #0a0a0f 100%);
      color: #e2e8f0;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
      background: linear-gradient(180deg, #111827 0%, #1a2235 100%);
      border-right: 1px solid #1e3a5f;
  }

  /* Chat messages */
  [data-testid="stChatMessage"] {
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(255,255,255,0.07);
      border-radius: 12px;
      margin-bottom: 8px;
      padding: 4px;
  }

  /* User message */
  [data-testid="stChatMessage"][data-testid*="user"] {
      background: rgba(59, 130, 246, 0.08);
      border-color: rgba(59, 130, 246, 0.2);
  }

  /* Input box */
  .stChatInputContainer {
      background: rgba(255,255,255,0.04) !important;
      border: 1px solid #1e3a5f !important;
      border-radius: 12px !important;
  }

  /* Headings */
  h1, h2, h3 {
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 700;
  }

  /* Tag badges */
  .skill-badge {
      display: inline-block;
      background: rgba(59, 130, 246, 0.15);
      border: 1px solid rgba(59, 130, 246, 0.4);
      color: #93c5fd;
      padding: 2px 10px;
      border-radius: 20px;
      font-size: 0.75rem;
      margin: 2px;
      font-family: 'JetBrains Mono', monospace;
  }

  /* Metric cards */
  [data-testid="metric-container"] {
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 10px;
      padding: 8px;
  }

  /* Divider */
  hr {
      border-color: rgba(255,255,255,0.07) !important;
  }

  /* Status indicator */
  .status-dot {
      width: 8px;
      height: 8px;
      background: #22c55e;
      border-radius: 50%;
      display: inline-block;
      margin-right: 6px;
      animation: pulse 2s infinite;
  }
  @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.4; }
  }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧑‍💻 Param Shah")
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
    <span class="skill-badge">🧮 Calculator</span>
    <span class="skill-badge">🌐 Web Search</span>
    <span class="skill-badge">🕐 Date & Time</span>
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
        '<div style="font-size:0.7rem; color:#64748b; text-align:center;">'
        'Built with LangChain · Groq · Gemini · ChromaDB<br>'
        '© 2024 Param Shah Digital Twin'
        '</div>',
        unsafe_allow_html=True,
    )


# ── Main header ────────────────────────────────────────────────────────────────
col_title, col_meta = st.columns([3, 1])
with col_title:
    st.markdown("# 🤖 Param Shah — Digital Twin")
    st.markdown(
        "An AI version of Param that talks like him, knows his resume, and can use tools. "
        "Ask anything — from his skills to live web searches!"
    )
with col_meta:
    st.markdown("&nbsp;")
    st.metric("🧠 LLM", "LLaMA-3.3-70B")
    st.metric("📦 Embeddings", "Gemini-001")
    st.metric("🗄️ VectorDB", "ChromaDB")

st.markdown("---")


# ── Session state init ─────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []          # for agent memory (dicts)
if "messages" not in st.session_state:
    st.session_state.messages = []              # for display (dicts)
if "agent_ready" not in st.session_state:
    st.session_state.agent_ready = False
if "agent_fn" not in st.session_state:
    st.session_state.agent_fn = None
if "pending_input" not in st.session_state:
    st.session_state.pending_input = None


# ── Agent initialization ───────────────────────────────────────────────────────
def initialize_agent(groq_api_key: str, gemini_api_key: str):
    """Build the vector store and agent, cache in session state."""
    from rag_setup import get_or_build_vector_store
    from agent import build_agent

    with st.spinner("🔨 Building RAG knowledge base from resume..."):
        vector_store = get_or_build_vector_store(gemini_api_key)
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    with st.spinner("🤖 Initializing Param's Digital Twin..."):
        agent_fn = build_agent(groq_api_key, retriever)

    st.session_state.agent_fn = agent_fn
    st.session_state.agent_ready = True

    # Welcome message
    welcome = (
        "Hey! 👋 I'm **Param Shah** — well, the AI version of me! "
        "I'm a Full Stack Developer currently pursuing my B.E. in Computer Engineering at GTU. "
        "Ask me anything about my skills, projects, or background — or give me a task like "
        "searching the web, doing math, or checking the time. Let's chat!"
    )
    st.session_state.messages.append({"role": "assistant", "content": welcome})


# ── Init button if keys present ────────────────────────────────────────────────
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
    # Handle sidebar example button clicks
    prefill = st.session_state.get("pending_input")
    if prefill:
        st.session_state.pending_input = None
        user_input = prefill
    else:
        user_input = st.chat_input("Ask Param anything... 💬")

    if user_input:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(user_input)

        # Get agent response
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

        # Update histories
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": response})

        st.rerun()
else:
    if not (groq_key and gemini_key):
        pass  # warning already shown above