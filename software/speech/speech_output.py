import pyttsx3
import sys
import os

# Add the parent directory to the path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import config
except ImportError:
    config = None

def speak(text: str):
    """
    Convert text to speech using pyttsx3.
    
    Args:
        text (str): The text to be spoken.
    """
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()
    
    # Try to select a female voice strictly
    voices = engine.getProperty('voices')
    voice_set = False
    
    # Pass 1: Look for explicit 'female' gender
    for voice in voices:
        if getattr(voice, 'gender', None) == 'female':
            engine.setProperty('voice', voice.id)
            voice_set = True
            break
            
    # Pass 2: Look for common female names in the voice ID/Name (Zira, Hazel)
    if not voice_set:
        for voice in voices:
            v_name = voice.name.lower()
            if 'female' in v_name or 'zira' in v_name or 'hazel' in v_name:
                engine.setProperty('voice', voice.id)
                voice_set = True
                break
                
    if not voice_set:
        print("Warning: Could not strictly identify a female voice profile on this system. Using default.")
    
    # Apply configuration settings if they are available
    if config:
        if hasattr(config, 'VOICE_RATE'):
            engine.setProperty('rate', config.VOICE_RATE)
        if hasattr(config, 'VOICE_VOLUME'):
            engine.setProperty('volume', config.VOICE_VOLUME)
            
    # Speak the provided text
    print(f"Speaking: '{text}'")
    engine.say(text)
    
    # Wait until speech completes
    engine.runAndWait()
