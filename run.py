from app import create_app
from app.schedules.scheduler import start

app = create_app()

if __name__ == "__main__":
    start()
    app.run(host="0.0.0.0", port=9090, debug=False)