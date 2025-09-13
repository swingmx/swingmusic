from flask import Response, stream_template_string, request
from flask_openapi3 import APIBlueprint

from swingmusic.events import events

api = APIBlueprint("sse", __name__, url_prefix="/events")


@api.route("/stream")
def stream_events():
    """
    Server-Sent Events endpoint for real-time updates.

    Returns:
        Streaming response with SSE format
    """
    # get origin from headers
    origin = request.headers.get("Origin")

    def event_stream():
        """Generator function for SSE stream."""
        for message_id, message_data in events.listen(timeout=5):
            # Format as SSE
            yield f"id: {message_id}\n"
            yield f"event: {message_data['type']}\n"
            yield f"data: {message_data}\n\n"

    return Response(
        event_stream(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "Cache-Control",
        },
    )


@api.route("/status")
def get_stats():
    """Get SSE connection statistics."""
    return {"active_listeners": events.get_listener_count()}
