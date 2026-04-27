import json
import os
from calendar_service import get_calendar_service, get_upcoming_events, create_event, update_event, \
    find_event_by_description
from openai_service import process_user_intent
from voice_interface import listen_for_command, speak_response


def format_events_response(events):
    """Formats calendar events into a readable message."""
    if not events:
        return "You have no upcoming events."

    response = "Here are your upcoming events:\n"
    for i, event in enumerate(events, 1):
        start = event['start'].get('dateTime', event['start'].get('date'))
        response += f"{i}. {event['summary']} - {start}\n"
    return response


def process_and_respond(service, user_input):
    """Process user input and execute appropriate calendar action."""
    gpt_response = process_user_intent(user_input)

    if not gpt_response:
        return "I'm having trouble understanding your request."

    function_call = gpt_response.choices[0].message.get('function_call')
    if function_call:
        function_name = function_call.get('name')
        arguments = json.loads(function_call.get('arguments', '{}'))

        if function_name == "check_calendar":
            events = get_upcoming_events(service)
            return format_events_response(events)

        elif function_name == "create_calendar_event":
            event = create_event(service, **arguments)
            if event:
                return f"Event created: {event['summary']}"
            return "Failed to create the event."

        elif function_name == "modify_calendar_event":
            event_id = find_event_by_description(service, arguments['event_identifier'])
            if event_id:
                updated_event = update_event(service, event_id, arguments['updates'])
                if updated_event:
                    return f"Event updated: {updated_event['summary']}"
            return "Couldn't find or update that event."

    return "I couldn't determine how to help with your calendar request."


def main():
    """Main application entry point."""
    service = get_calendar_service()

    use_voice = input("Do you want to use voice interface? (yes/no): ").lower() == "yes"

    while True:
        if use_voice:
            user_input = listen_for_command()
            if not user_input:
                continue
        else:
            user_input = input("\nHow can I help with your calendar? (type 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break

        response = process_and_respond(service, user_input)

        if use_voice:
            speak_response(response)
        print(response)


if __name__ == "__main__":
    main()