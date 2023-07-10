import requests
import uvicorn
from app.app import app
from app.endpoints import KNOWLEDGE_URL, PROCESSES_URL

def on_start():
    try:
        return {
            "knowledge": requests.get(KNOWLEDGE_URL + "/health").status_code == 200,
            "processes": requests.get(PROCESSES_URL + "/health").status_code == 200
        }
    except Exception as e:
        print(f"relevant processes arn't running {e}")
        return False

if __name__ == "__main__":
    if on_start():
        uvicorn.run("app.app:app", host="0.0.0.0", port=9005, log_level="info", reload=True)
    
    # Run the second app on port 9001
    #uvicorn.run(app2, host="0.0.0.0", port=9001, log_level="info")