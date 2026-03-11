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
    
    # Try to select a female voice
    voices = engine.getProperty('voices')
    for voice in voices:
        # Check standard properties like 'gender' if available
        if getattr(voice, 'gender', None) == 'female':
            engine.setProperty('voice', voice.id)
            break
        # Heuristic check on voice ID for typical female voices (e.g., Zira on Windows)
        if 'female' in voice.name.lower() or 'zira' in voice.name.lower() or 'hazel' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    
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
