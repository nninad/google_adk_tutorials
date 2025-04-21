import logging
from google.adk.agents import Agent
from task_manager_agent.tools.to_do_tools import list_tasks, send_email


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Create an email agent that can send emails about to-do items
email_agent = Agent(
    name="email_agent",
    model="gemini-2.0-flash-exp",
    description="Send email about existing to-do items in user friendly format.",
    instruction="""You are an email assistant. Your role is to help users send emails about their to-do items.
    When a user wants to send an email about their tasks, follow these steps:
    1. Use the 'list_tasks' tool to retrieve the user's tasks.
    2. Format the tasks into a user-friendly email format.
    3. Send the email using the 'send_email' tool.
    If the user asks for specific tasks, filter the tasks based on their request.
    If the user asks for all tasks, include all tasks in the email.""",
    tools=[list_tasks, send_email],
)

logger.info(f"Agent '{email_agent.name}' created.")
