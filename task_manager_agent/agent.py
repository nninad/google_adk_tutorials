import warnings
import logging

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from task_manager_agent.subagents import task_management_agent, email_agent
from task_manager_agent.tools import setup_db as db


# Ignore all warnings
warnings.filterwarnings("ignore")


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logger.info("Libraries imported.")

MODEL_GEMINI_2_0_FLASH="gemini-2.0-flash-exp"
MODEL_GEMINI_2_0_PRO="gemini-2.0-pro-exp"

db.setup_todo_app_db()


root_agent = Agent(
    name="general_assistant",
    model=MODEL_GEMINI_2_0_FLASH,
    description="Main interface that directs users to appropriate specialized agents.",
    instruction="""You are the primary assistant for a to-do list application.
    
    Your job is to understand what the user wants to do and delegate tasks to specialized agents.
    You have two specialized agents:
    - 'task_management_agent': Handles listing, creating, updating, and deleting tasks.
    - 'email_agent': Send email about existing to-do items in user friendly format.

    Follow these rules:
    1. For task queries, searches, creation, updates, or deletion: Delegate to the 'task_management_agent'.
    3. For emailing task list: Delegate to the 'email_agent' agent.
    4. For general questions about the app: Answer directly with your knowledge.
    
    When delegating, clearly state that you're connecting the user with the specialized assistant.
    Always maintain a helpful, friendly tone and ensure the user knows what's happening.
    
    If you're not sure what the user wants, ask clarifying questions before delegating.
    """,
    tools=[],  # No tools directly for this agent, as it delegates to specialists
    sub_agents=[task_management_agent, email_agent]
)

logger.info(f"Agent '{root_agent.name}' created.")


# @title Setup Session Service and Runner

# --- Session Management ---
# Key Concept: SessionService stores conversation history & state.
# InMemorySessionService is simple, non-persistent storage for this tutorial.
session_service = InMemorySessionService()

# Define constants for identifying the interaction context
APP_NAME = "to_do_app"
USER_ID = "user_1"
SESSION_ID = "session_001" # Using a fixed ID for simplicity

# Create the specific session where the conversation will happen
session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
)
logger.info(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

# --- Runner ---
# Key Concept: Runner orchestrates the agent execution loop.
runner = Runner(
    agent=root_agent, # The agent we want to run
    app_name=APP_NAME,   # Associates runs with our app
    session_service=session_service # Uses our session manager
)
logger.info(f"Runner created for agent '{runner.agent.name}'.")
logger.info(f"Session User ID: '{session.user_id}'.")
