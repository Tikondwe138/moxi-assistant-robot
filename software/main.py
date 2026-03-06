import time
import sys
import os

# Import custom modules
from speech.speech_listener import listen
from speech.speech_output import speak
from services.inventory_api import check_inventory_batch
from services.contacts_service import get_contact
from robot_control.arm_controller import trigger_gesture, get_controller
from nlp.intent_parser import parse_intent
from utils.logger import setup_logger

from dashboard.app import start_dashboard

logger = setup_logger("main_core")

def execute_intent(intent_data: dict, dashboard_updater) -> bool:
    """Executes the mapped NLP intent string to a physical/verbal action."""
    intent = intent_data.get("intent")
    entities = intent_data.get("entities", [])
    
    dashboard_updater("last_command", f"Intent: {intent}")
    logger.info(f"Executing intent: {intent} with entities: {entities}")
    
    if intent == "greeting":
        speak("Hello! I am MOXI. I'm ready to assist you in the studio today.")
        trigger_gesture("WAVE")
        
    elif intent == "contact_lookup":
        if entities:
            name = entities[0]
            phone = get_contact(name)
            if phone.startswith("Error"):
                speak(f"I'm sorry, I could not find {name} in the contact directory.")
            else:
                speak(f"I found {name}. Their phone number is {phone}.")
        else:
            speak("Who are you looking for?")
            
    elif intent == "inventory_check":
        if entities:
            items_phrase = " and ".join(entities)
            speak(f"Let me check the inventory for {items_phrase}.")
            
            # Batch API call processing 
            availability_dict = check_inventory_batch(entities)
            
            for item, is_avail in availability_dict.items():
                if is_avail:
                    speak(f"Yes, {item} is available in the studio.")
                else:
                    speak(f"No, {item} is currently out of stock.")
                    
            dashboard_updater("inventory_api_status", "Query Successful")
        else:
            speak("What items are you looking for?")
            
    elif intent == "gesture_command":
        # Check if the user specified the gesture ("point", "thumbsup")
        target_gesture = "WAVE" 
        for ent in entities:
             if ent in ["point", "wave", "thumbsup"]:
                 target_gesture = ent.upper()
                 
        speak(f"Executing {target_gesture} gesture.")
        trigger_gesture(target_gesture)
        
    elif intent == "exit":
        speak("Shutting down MOXI core system. Goodbye!")
        # Clean up serial queue
        get_controller().close()
        return False
        
    else:
         speak("I didn't quite catch the intent. Could you rephrase your request?")
         
    return True


def main():
    """Central controller loop with Background Dashboard and AI Intending."""
    logger.info("Starting MOXI Core Engine v2.0")
    
    # Init dashboard thread
    update_dashboard = start_dashboard()
    time.sleep(1) # Give flash thread time to bind port
    
    update_dashboard("status", "Online")
    update_dashboard("inventory_api_status", "Idle")
    
    speak("System ready. MOXI is online and listening for commands.")
    running = True
    
    try:
        while running:
            # 1. Capture Multi-Commands via Speech Listener (Yields list of phrases)
            command_list = listen(timeout=4, max_failures=1)
            
            # Note: We skipped automatic wave detection inside the main loop to prevent
            # blocking. The dashboard manual REST trigger overrides show integration.
            # Usually vision tracking would go into a parallel multiprocessing pipe.
            
            # 2. Process all captured phrases consecutively
            for command_text in command_list:
                if not running: break
                
                print(f"Raw Speech Captured: {command_text}")
                # 3. Classify AI Intent using spaCy
                intent_data = parse_intent(command_text)
                
                # 4. Trigger logical action and UI update
                running = execute_intent(intent_data, update_dashboard)
                
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt.")
    except Exception as e:
        logger.error(f"Fatal error in main loop: {e}", exc_info=True)
        update_dashboard("status", "Error/Crashed")
    finally:
        logger.info("MOXI Core Terminated")
        get_controller().close()

if __name__ == "__main__":
    main()
