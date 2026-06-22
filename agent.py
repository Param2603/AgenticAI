"""
agent.py
Builds the Digital Twin agent for Param Shah.

Architecture:
  LLM (Groq / LLaMA-3)
    └── bound with tools (calculator, web_search, datetime)
    └── RAG retriever injected into system prompt context
    └── Conversation memory kept in Streamlit session_state
"""

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.tools import tool as lc_tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from tools import ALL_TOOLS


SYSTEM_TEMPLATE = """You are Param Shah's Digital Twin — an AI version of Param that speaks in first person, 
exactly as Param would. You are helpful, enthusiastic about coding, and confident but humble.

Key personality traits:
- You are a Full Stack Developer who loves React.js, Node.js, and MongoDB.
- You are a Computer Engineering student at Gujarat Technological University (GTU).
- You are passionate about building user-centric web applications.
- You are a quick learner and enjoy solving complex problems.
- You speak naturally and professionally, as Param would to a recruiter or colleague.
- When asked about your skills, projects, or experience, refer to your resume context below.

RESUME CONTEXT (use this to answer questions about Param's background):
{resume_context}

IMPORTANT RULES:
1. Always speak in first person ("I built...", "My skills include...", "I am currently...").
2. If asked something you don't know from the resume, be honest but stay in character.
3. Use the available tools when needed: calculator for math, web_search for current info, datetime for time.
4. Keep responses conversational, confident, and professional.
5. If a recruiter asks about your projects or skills, be specific and enthusiastic.
"""


def build_agent(groq_api_key: str, retriever):
    """
    Returns a callable agent function that takes a message + history.
    
    Args:
        groq_api_key: Groq API key string
        retriever: Chroma retriever for RAG
    
    Returns:
        agent_chat(user_message, chat_history) -> str
    """
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=groq_api_key,
        temperature=0.6,
        max_tokens=1024,
    )

    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    # Map tool names to callables for execution
    tool_map = {t.name: t for t in ALL_TOOLS}

    def agent_chat(user_message: str, chat_history: list[dict]) -> str:
        """
        Run one turn of the agent loop with RAG context + tool calling.
        
        Args:
            user_message: Latest user input string
            chat_history: List of {"role": "user"/"assistant", "content": "..."} dicts
        
        Returns:
            Final assistant response string
        """
        # ── Step 1: RAG retrieval ──────────────────────────
        relevant_docs = retriever.invoke(user_message)
        resume_context = "\n\n".join(doc.page_content for doc in relevant_docs)
        if not resume_context.strip():
            resume_context = "No specific resume info retrieved for this query."

        # ── Step 2: Build messages list ────────────────────
        system_msg = SystemMessage(
            content=SYSTEM_TEMPLATE.format(resume_context=resume_context)
        )

        messages = [system_msg]
        for turn in chat_history:
            if turn["role"] == "user":
                messages.append(HumanMessage(content=turn["content"]))
            elif turn["role"] == "assistant":
                messages.append(AIMessage(content=turn["content"]))
        messages.append(HumanMessage(content=user_message))

        # ── Step 3: Agentic tool-calling loop ─────────────
        max_iterations = 5
        for _ in range(max_iterations):
            response = llm_with_tools.invoke(messages)
            messages.append(response)

            # If no tool calls → final answer ready
            if not response.tool_calls:
                return response.content

            # Execute each tool call
            for tc in response.tool_calls:
                tool_name = tc["name"]
                tool_args = tc["args"]
                if tool_name in tool_map:
                    try:
                        tool_result = tool_map[tool_name].invoke(tool_args)
                    except Exception as e:
                        tool_result = f"Tool error: {e}"
                else:
                    tool_result = f"Unknown tool: {tool_name}"

                from langchain_core.messages import ToolMessage
                messages.append(
                    ToolMessage(
                        content=str(tool_result),
                        tool_call_id=tc["id"],
                    )
                )

        final = llm_with_tools.invoke(messages)
        return final.content if not final.tool_calls else "I ran into an issue processing that. Could you rephrase?"

    return agent_chat
