# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []




from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Full-time credit hour requirements
CREDIT_REQUIREMENTS = {
    "Fall": {"undergrad": 12, "grad": 9},
    "Spring": {"undergrad": 12, "grad": 9},
    "Summer": {"undergrad": 6, "grad": 5},
    "Spring A": {"undergrad": 3, "grad": 3},
    "Spring B": {"undergrad": 3, "grad": 3},
    "Fall A": {"undergrad": 3, "grad": 3},
    "Fall B": {"undergrad": 3, "grad": 3},
}

class ActionCheckFullTimeStatus(Action):
    def name(self) -> Text:
        return "action_check_full_time_status"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        semester = tracker.get_slot("semester")
        credit_hours = tracker.get_slot("credit_hours")

        # Ask user if semester is missing
        if not semester:
            dispatcher.utter_message(text="Which semester are you asking about? (Spring, Summer, Fall, A/B terms)")
            return []

        # Ask user for credit hours if missing
        if not credit_hours:
            dispatcher.utter_message(text="How many credit hours are you taking?")
            return []

        # Normalize semester name
        semester = semester.title()  # Convert "spring" -> "Spring"

        if semester not in CREDIT_REQUIREMENTS:
            dispatcher.utter_message(text="I didn't recognize that semester. Please specify Spring, Summer, Fall, or A/B terms.")
            return []

        # Determine full-time requirement
        undergrad_full_time = CREDIT_REQUIREMENTS[semester]["undergrad"]
        grad_full_time = CREDIT_REQUIREMENTS[semester]["grad"]

        # Response for both undergrad and grad levels
        response = f"For {semester}, full-time status is:\n- Undergraduate: {undergrad_full_time} credits\n- Graduate: {grad_full_time} credits.\n"

        if float(credit_hours) >= undergrad_full_time:
            response += "✅ You are full-time for undergrad."
        elif float(credit_hours) >= grad_full_time:
            response += "✅ You are full-time for graduate level."
        else:
            response += "❌ You are considered part-time."

        dispatcher.utter_message(text=response)
        return []
