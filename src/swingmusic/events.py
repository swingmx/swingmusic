import threading
import time
import queue
from typing import Dict, Any, Generator, Tuple, Optional
from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Event:
    id: str
    type: str
    data: Any
    timestamp: float


class Events:
    def __init__(self):
        self._listeners: Dict[str, queue.Queue] = {}
        self._lock = threading.Lock()
        self._message_counter = 0
        
    def dispatch(self, event_type: str, data: Any) -> None:
        """
        Dispatch an event to all listeners.
        
        Args:
            event_type: The type of event (e.g., 'track_changed', 'playlist_updated')
            data: The data to send with the event
        """
        event = Event(
            id=str(self._message_counter),
            type=event_type,
            data=data,
            timestamp=time.time()
        )
        
        with self._lock:
            self._message_counter += 1
            
            # Send to all active listeners
            dead_listeners = []
            for listener_id, listener_queue in self._listeners.items():
                try:
                    listener_queue.put_nowait(event)
                except queue.Full:
                    # Remove listeners with full queues (probably disconnected)
                    dead_listeners.append(listener_id)
            
            # Clean up dead listeners
            for listener_id in dead_listeners:
                del self._listeners[listener_id]
    
    def listen(self, timeout: Optional[float] = None) -> Generator[Tuple[str, Any], None, None]:
        """
        Generator that yields (message_id, message_data) for SSE consumption.
        
        Args:
            timeout: How long to wait for new events (None = block indefinitely)
            
        Yields:
            Tuple of (message_id, message_data)
        """
        listener_id = str(uuid4())
        listener_queue = queue.Queue(maxsize=100)  # Prevent memory issues
        
        with self._lock:
            self._listeners[listener_id] = listener_queue
        
        try:
            while True:
                try:
                    event = listener_queue.get(timeout=timeout)
                    yield event.id, {
                        'type': event.type,
                        'data': event.data,
                        'timestamp': event.timestamp
                    }
                except queue.Empty:
                    # Send heartbeat to keep connection alive
                    yield str(self._message_counter), {'type': 'heartbeat', 'data': None, 'timestamp': time.time()}
                    
        except (GeneratorExit, StopIteration, Exception):
            # Client disconnected or other error, clean up
            pass
        finally:
            # Always clean up listener when generator exits
            with self._lock:
                if listener_id in self._listeners:
                    del self._listeners[listener_id]
    
    def get_listener_count(self) -> int:
        """Get the number of active listeners."""
        with self._lock:
            return len(self._listeners)
    
    def clear_listeners(self) -> None:
        """Remove all listeners (useful for testing or shutdown)."""
        with self._lock:
            self._listeners.clear()


# Global events instance
events = Events()