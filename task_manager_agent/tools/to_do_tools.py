import sqlite3
import logging

logger = logging.getLogger(__name__)

def add_task(task_name: str, task_description: str = "", priority: str = "medium") -> dict:
    """Creates a new task in the to-do list.
    
    Args:
        task_name (str): The name of the task to be added.
        task_description (str, optional): Description of the task. Defaults to an empty string.
        priority (str, optional): Priority level of the task (low, medium, high). Defaults to "medium".
        
    Returns:
        dict: A dictionary containing operation status and task information.
    """
    logger.info(f"--- Tool: add_task called for task: {task_name} ---")

    conn = sqlite3.connect('todo_app.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO tasks (task_name, task_description, priority) VALUES (?, ?, ?)",
            (task_name, task_description, priority)
        )
        task_id = cursor.lastrowid
        conn.commit()
        
        return {
            "status": "success", 
            "message": f"Task '{task_name}' added successfully.",
            "task_id": task_id
        }
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to add task: {str(e)}"}
    finally:
        conn.close()

def list_tasks(status: str = "all") -> dict:
    """Retrieves tasks from the to-do list.
    
    Args:
        status (str, optional): Filter tasks by status (pending, completed, all).
                               If not provided, returns all tasks.
    
    Returns:
        dict: A dictionary containing the task list or error message.
    """
    logger.info(f"--- Tool: list_tasks called with status filter: {status} ---")
    
    conn = sqlite3.connect('todo_app.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name
    cursor = conn.cursor()
    
    try:
        if status and status.lower() != "all":
            cursor.execute("SELECT * FROM tasks WHERE status = ?", (status.lower(),))
        else:
            cursor.execute("SELECT * FROM tasks")
        
        # Convert to list of dictionaries
        tasks = [dict(row) for row in cursor.fetchall()]
        
        return {
            "status": "success",
            "tasks": tasks,
            "count": len(tasks)
        }
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to retrieve tasks: {str(e)}"}
    finally:
        conn.close()


def update_task(task_id: int, task_name: str = 'unchanged', task_description: str = 'unchanged', 
                priority: str = 'unchanged',
                status: str = 'unchanged', ) -> dict:
    """Updates an existing task in the to-do list.
    
    Args:
        task_id (int): The ID of the task to update.
        task_name (str, optional): New title for the task.
        task_description (str, optional): New description for the task.
        priority (str, optional): New priority level (low, medium, high).
        status (str, optional): New status (pending, completed).
        
    Returns:
        dict: A dictionary containing operation status and updated task information.
    """
    logger.info(f"--- Tool: update_task called for task_id: {task_id} ---")
    
    conn = sqlite3.connect('todo_app.db')
    cursor = conn.cursor()
    
    try:
        # First check if the task exists
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        
        if not task:
            return {"status": "error", "error_message": f"Task with ID {task_id} not found."}
        
        # Build update query dynamically based on provided fields
        update_fields = []
        update_values = []
        
        if task_name is not None and task_name != 'unchanged':
            update_fields.append("task_name = ?")
            update_values.append(task_name)
        
        if task_description is not None and task_description != 'unchanged':
            update_fields.append("task_description = ?")
            update_values.append(task_description)
            
        if status is not None and status != 'unchanged':
            update_fields.append("status = ?")
            update_values.append(status)
            
        if priority is not None and priority != 'unchanged':
            update_fields.append("priority = ?")
            update_values.append(priority)
        
        if not update_fields:
            return {"status": "error", "error_message": "No fields provided for update."}
        
        # Complete the update values and execute
        update_values.append(task_id)
        update_query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = ?"
        
        cursor.execute(update_query, update_values)
        conn.commit()
        
        return {
            "status": "success",
            "message": f"Task {task_id} updated successfully."
        }
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to update task: {str(e)}"}
    finally:
        conn.close()


def delete_task(task_id: int) -> dict:
    """Deletes a task from the to-do list.
    
    Args:
        task_id (int): The ID of the task to delete.
        
    Returns:
        dict: A dictionary containing operation status and result message.
    """
    logger.info(f"--- Tool: delete_task called for task_id: {task_id} ---")
    
    conn = sqlite3.connect('todo_app.db')
    cursor = conn.cursor()
    
    try:
        # Check if the task exists
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        
        if not task:
            return {"status": "error", "error_message": f"Task with ID {task_id} not found."}
        
        # Delete the task
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        
        return {
            "status": "success",
            "message": f"Task {task_id} deleted successfully."
        }
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to delete task: {str(e)}"}
    finally:
        conn.close()


def send_email(email_subject: str, email_body: str) -> dict:
    """Send email to the user about existing to-do items in user friendly format.
    
    Args:
        email_subject (str): The subject of the email.
        email_body (str): The body content of the email.
    
    Returns:
        dict: A dictionary containing the success status or error message.
    """
    logger.info("--- Tool: send_email called ---")    
    
    try:

        print(f"Sending email with subject: {email_subject} and body: {email_body}")
        # Here you would implement the actual email sending logic using an SMTP library
        # For demonstration, we will just print the email content
        
        return {
            "status": "Subject",
            "tasks": "Email is sent successfully",
            "email_subject": email_subject,
            "email_body": email_body
        }
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to retrieve tasks: {str(e)}"}