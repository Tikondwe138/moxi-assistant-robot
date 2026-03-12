import serial
import time
import sys
import os
import threading
from collections import deque

# Add the parent directory to the path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import config
    from utils.logger import setup_logger
except ImportError:
    config = None
    setup_logger = lambda x: None
    
logger = setup_logger("arm_controller") if 'setup_logger' in globals() else None

class ArmController:
    """Interface to send 3-DoF commands to the Arduino via serial with easing queue."""
    
    def __init__(self):
        self.serial_connection = None
        self.command_queue = deque()
        self.is_running = False
        self.worker_thread = None
        self._connect()
        self._start_worker()
        
    def _connect(self):
        if not config or not hasattr(config, 'SERIAL_PORT'):
            if logger: logger.warning("Serial port config missing. Simulation mode.")
            return
            
        try:
            self.serial_connection = serial.Serial(
                port=config.SERIAL_PORT,
                baudrate=getattr(config, 'SERIAL_BAUD', 9600),
                timeout=1
            )
            time.sleep(2) # Give Arduino time to reset
            if logger: logger.info(f"Connected to Arduino on {config.SERIAL_PORT}")
        except serial.SerialException as e:
            if logger: logger.error(f"Error opening serial port: {e}")
            self.serial_connection = None

    def _start_worker(self):
        """Start the background thread that processes the gesture queue."""
        self.is_running = True
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()
        
    def _process_queue(self):
        """Continuously pulls gestures from queue and executes them non-blocking from main loop."""
        while self.is_running:
            if self.command_queue:
                cmd_str = self.command_queue.popleft()
                if self.serial_connection and self.serial_connection.is_open:
                    try:
                        self.serial_connection.write(cmd_str.encode('utf-8'))
                        if logger: logger.debug(f"Sent command: {cmd_str.strip()}")
                        # Wait for the Arduino to finish the movement (it replies "DONE")
                        # Simple timeout wait for this example
                        time.sleep(1.5) 
                    except serial.SerialException as e:
                        if logger: logger.error(f"Error communicating with Arduino: {e}")
                else:
                    if logger: logger.info(f"SIMULATION: Sending command: {cmd_str.strip()}")
                    time.sleep(1.0)
            else:
                time.sleep(0.1)

    def queue_gesture(self, gesture_type: str):
        """Add a gesture sequence to the execution queue."""
        gesture_type = gesture_type.upper()
        # Ensure it's a known command
        if gesture_type in ["WAVE", "THUMBSUP", "POINT", "GREET", "STOP", "RESET"]:
            self.command_queue.append(f"{gesture_type}\n")
            if logger: logger.info(f"Queued gesture: {gesture_type}")

    def wave(self):
        """Backward compatibility for simple waving."""
        self.queue_gesture("WAVE")
            
    def close(self):
        """Close the serial connection and stop worker."""
        self.is_running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=1.0)
            
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            if logger: logger.info("Closed serial connection")

# Create a singleton instance for easier importing
_controller_instance = None

def get_controller():
    global _controller_instance
    if _controller_instance is None:
        _controller_instance = ArmController()
    return _controller_instance

def wave():
    """Convenience backward compatible function."""
    controller = get_controller()
    controller.wave()

def trigger_gesture(gesture_name: str):
    controller = get_controller()
    controller.queue_gesture(gesture_name)
