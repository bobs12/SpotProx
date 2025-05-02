
from flask import Flask, request, jsonify
from proxmoxer import ProxmoxAPI
from config import PROXMOX_HOST, PROXMOX_USER, PROXMOX_PASS, PROXMOX_NODE
#from storage import load_instances, save_instances
import uuid
from datetime import datetime, timedelta, timezone
import json
import time

proxmox = None
app = Flask(__name__)


def get_proxmox():
    if proxmox is None:
        print("⚠️ Proxmox connection is not available.")
        return None
    return proxmox


@app.route("/networks")
def networks():
    raw_data = load_network()  # ← твоя функція, яка читає JSON
    networks = []

    for key, net in raw_data.items():
        network = {
            "id": key,
            "name": net.get("iface", key),
            "subnet": f"{net.get('address', '')}/{net.get('netmask', '')}",
            "vms": net.get("vms", [])  # список машин, які мають бути вручну привʼязані
        }
        networks.append(network)

    return render_template("networks.html", networks=networks)

@app.route("/network/health", methods=["GET"])
def healthcheck():
    return jsonify({"status": "200"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)