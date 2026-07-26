import json
from datetime import datetime

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            # Convert datetime to a string representation
            return obj.isoformat()
        # Extend this for other data types if needed
        return super().default(obj)