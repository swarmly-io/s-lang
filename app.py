import uvicorn
from app.app import app

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=9005, log_level="info", reload=True)
    
    # Run the second app on port 9001
    #uvicorn.run(app2, host="0.0.0.0", port=9001, log_level="info")