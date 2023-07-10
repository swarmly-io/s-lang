from app.app import app

@app.get("test/init")
def test_init():
    pass

scenarios = {
    "zombie_near": "",
    "health_low": ""
}

@app.get("/")
def init():
    pass

