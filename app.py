import requests
import uvicorn
from app.app import app
from app.endpoints import KNOWLEDGE_URL, ENTITIES_URL

def on_start():
    try:
        return {
            "knowledge": requests.get(KNOWLEDGE_URL + "/health").status_code == 200,
            "entities": requests.get(ENTITIES_URL + "/health").status_code == 200
        }
    except Exception as e:
        print(f"relevant processes arn't running {e}")
        return False

if __name__ == "__main__":
    if on_start():
        uvicorn.run("app.app:app", host="0.0.0.0", port=9005, log_level="info", reload=True)