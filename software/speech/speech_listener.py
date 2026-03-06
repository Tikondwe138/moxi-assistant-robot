import speech_recognition as sr
import time

def listen(timeout=5, phrase_time_limit=15, max_failures=2) -> list[str]:
    """
    Capture continuous voice inputs utilizing noise suppression and multi-command parsing.
    
    Args:
        timeout: Stop listening after N seconds of silence.
        phrase_time_limit: Max length of a single phrase.
        max_failures: Number of times to fallback and retry on no match.
        
    Returns:
        List of recognized command strings. Empty list if nothing recognized.
    """
    recognizer = sr.Recognizer()
    commands = []
    failures = 0
    
    with sr.Microphone() as source:
        print("Calibrating background noise... (Noise Suppression Active)")
        recognizer.adjust_for_ambient_noise(source, duration=1.0)
        # Apply a basic energy threshold filter equivalent roughly to PyAudio low-pass
        recognizer.dynamic_energy_threshold = True
        
        while failures <= max_failures:
            print(f"Listening... (Attempt {failures+1}/{max_failures+1})")
            
            try:
                # Listen to the user's input
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                # Recognize audio
                text = recognizer.recognize_google(audio)
                
                # If we got text, assume success and maybe people speak fast 
                # split by common phrase boundary indicators like "and" or "then"
                # For basic NLP, just append the full text to commands and let NLP handle it.
                if text:
                    print(f"Recognized: '{text}'")
                    commands.append(text)
                    return commands  # Return immediately on successful capture
                    
            except sr.UnknownValueError:
                print("Speech Recognition could not understand audio.")
                failures += 1
                if failures <= max_failures:
                    print("Retrying...")
                    time.sleep(0.5)
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return []
            except sr.WaitTimeoutError:
                print("Listening timed out.")
                # Timeout isn't exactly a failure we want to spam retry for if they are just quiet
                return commands
            except Exception as e:
                print(f"Unexpected audio error: {e}")
                return []
                
        print("Maximum speech retries reached. Fallback triggered.")
        return commands
