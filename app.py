from flask import Flask, request, jsonify
from flask_cors import CORS
import socket

app = Flask(__name__)
CORS(app) # Crucial for your frontend connection

@app.route("/api/scan", methods=["POST"])
def scan_ports():
    data = request.get_json() or {}
    host = data.get("host", "").replace("https://", "").replace("http://", "").strip("/")
    ports_string = data.get("ports", "")
    timeout = float(data.get("timeout", 1.0))

    if not host:
        return jsonify({"detail": "Missing host target"}), 400

    try:
        target_ip = socket.gethostbyname(host)
    except socket.gaierror:
        return jsonify({"detail": "Cannot resolve host domain or IP."}), 400

    try:
        port_list = [int(p.strip()) for p in ports_string.split(",") if p.strip()]
    except ValueError:
        return jsonify({"detail": "Invalid port format."}), 400

    results = []
    for port in port_list:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            result = s.connect_ex((target_ip, port))
            results.append({"port": port, "status": "OPEN" if result == 0 else "CLOSED"})
            s.close()
        except Exception:
            results.append({"port": port, "status": "ERROR"})

    return jsonify({"host": host, "ip": target_ip, "results": results})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)