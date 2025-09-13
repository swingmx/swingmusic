# Example usage of the Events system

from swingmusic.events import events
import time
import threading

# Example 1: Dispatching events from anywhere in your app
def track_changed_handler(track_id, track_name):
    """Example function that dispatches an event when a track changes"""
    events.dispatch("track_changed", {
        "track_id": track_id,
        "track_name": track_name,
        "timestamp": time.time()
    })

# Example 2: Playlist update event
def playlist_updated_handler(playlist_id, action, track_count):
    """Example function for playlist updates"""
    events.dispatch("playlist_updated", {
        "playlist_id": playlist_id,
        "action": action,  # "added", "removed", "reordered"
        "track_count": track_count
    })

# Example 3: User activity event
def user_activity_handler(user_id, activity_type, details):
    """Example function for user activity tracking"""
    events.dispatch("user_activity", {
        "user_id": user_id,
        "activity_type": activity_type,
        "details": details
    })

# Example 4: System notification
def system_notification_handler(message, level="info"):
    """Example function for system notifications"""
    events.dispatch("notification", {
        "message": message,
        "level": level,  # "info", "warning", "error"
        "timestamp": time.time()
    })

# Example usage in your Flask routes or background tasks:
if __name__ == "__main__":
    # Simulate some events being dispatched
    def simulate_events():
        time.sleep(1)
        track_changed_handler("track123", "Bohemian Rhapsody")
        time.sleep(2)
        playlist_updated_handler("playlist456", "added", 15)
        time.sleep(1)
        system_notification_handler("Library scan completed", "info")
        time.sleep(3)
        user_activity_handler("user789", "play", {"track_id": "track123"})
    
    # Start simulation in background
    threading.Thread(target=simulate_events, daemon=True).start()
    
    # Example of consuming events (this would normally be in your SSE endpoint)
    print("Listening for events...")
    for msg_id, msg_data in events.listen(timeout=10):
        print(f"Event {msg_id}: {msg_data}")
        # In real SSE, this would be formatted and sent to client