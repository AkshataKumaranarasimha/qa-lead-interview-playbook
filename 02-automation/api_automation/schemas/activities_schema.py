"""JSON schemas for Activities API responses"""

ACTIVITIES_LIST_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": ["integer", "string"]},
            "title": {"type": "string"},
            "description": {"type": ["string", "null"]},
            "status": {"type": "string"},
            "createdAt": {"type": "string"},
            "updatedAt": {"type": ["string", "null"]}
        },
        "required": ["id", "title"]
    }
}

ACTIVITY_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": ["integer", "string"]},
        "title": {"type": "string"},
        "description": {"type": ["string", "null"]},
        "status": {"type": "string"},
        "createdAt": {"type": "string"},
        "updatedAt": {"type": ["string", "null"]}
    },
    "required": ["id", "title"]
}
