import json
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def process_user_intent(user_input):
    """Uses OpenAI GPT to understand user intent."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI assistant that helps users manage their Google Calendar. Extract the user's intent and relevant details from their input."},
                {"role": "user", "content": user_input}
            ],
            functions=[
                {
                    "name": "check_calendar",
                    "description": "Check upcoming events in the calendar",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "time_period": {"type": "string", "description": "The time period to check (today, tomorrow, this week, etc.)"},
                            "max_results": {"type": "integer", "description": "Maximum number of events to return"}
                        }
                    }
                },
                {
                    "name": "create_calendar_event",
                    "description": "Create a new calendar event",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "summary": {"type": "string", "description": "Event title"},
                            "start_time": {"type": "string", "description": "Start time of the event (ISO format)"},
                            "end_time": {"type": "string", "description": "End time of the event (ISO format)"},
                            "description": {"type": "string", "description": "Event description"},
                            "location": {"type": "string", "description": "Event location"}
                        },
                        "required": ["summary", "start_time", "end_time"]
                    }
                },
                {
                    "name": "modify_calendar_event",
                    "description": "Modify an existing calendar event",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "event_identifier": {"type": "string", "description": "Description of the event to modify"},
                            "updates": {
                                "type": "object",
                                "properties": {
                                    "summary": {"type": "string"},
                                    "start_time": {"type": "string"},
                                    "end_time": {"type": "string"},
                                    "description": {"type": "string"},
                                    "location": {"type": "string"}
                                }
                            }
                        },
                        "required": ["event_identifier", "updates"]
                    }
                }
            ],
            function_call="auto"
        )
        return response
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return None