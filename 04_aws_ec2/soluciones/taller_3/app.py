
from flask import Flask
from datetime import datetime, timezone
import socket
import os

app = Flask(__name__)

@app.get("/")
def home():
    return {
        "message": "Hola desde EC2",
        "contenedor_hostname": socket.gethostname(),
        "ec2_hostname": os.environ.get("EC2_HOSTNAME", "No configurado"),
        "hora_actual": datetime.now(timezone.utc).isoformat()
    }

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

