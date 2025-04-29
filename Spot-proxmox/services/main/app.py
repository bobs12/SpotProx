
import threading
from flask import Flask, render_template, request, redirect, url_for
import requests
#from services.spot.spot import spot_vm,load_instances, manage_power_from_schedule, delete_vm, load_instances, get_instances_with_live_status

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/networks")
def network():
    return render_template("network.html")

@app.route("/spot")
def index():
    try:
        response = requests.get("http://spot-service:5001/list")
        response.raise_for_status()
        instances = response.json()
    except Exception as e:
        print(f"⚠️ Failed to get instances from spot-service: {e}")
        instances = []

    return render_template("darktheme.html", instances=instances)

   
@app.route("/create", methods=["POST"])
def create():
    name = request.form["name"]

    template = int(request.form["template"])
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]
    data = {
        "name": name,
        "template": template,
        "start_time": start_time,
        "end_time": end_time
    }
    try:
            res = requests.post("http://spot-service:5001/create", json=data)
            res.raise_for_status()  # якщо помилка, підніме виключення
    except requests.exceptions.RequestException as e:
            print(f"Error sending create request: {e}")
            return "Failed to create VM", 500
    #spot_vm(vm_id=name,vm_name=name,vm_template=template, start_time=start_time, end_time=end_time,duration=1)
    return redirect(url_for("index"))

@app.route("/start/<int:vmid>", methods=["POST"])
def start(vmid):
    start_vm(vmid)
    return redirect(url_for("index"))

@app.route("/stop/<int:vmid>", methods=["POST"])
def stop(vmid):
    stop_vm(vmid)
    return redirect(url_for("index"))

@app.route("/delete/<int:vmid>", methods=["POST"])
def delete(vmid):
    delete_vm(vmid)
    return redirect(url_for("index"))

@app.route("/status/<int:vmid>", methods=["GET"])
def status(vmid):
    try:
        res = requests.get(f"http://spot-service:5001/status/{vmid}")
        res.raise_for_status()
        status_info = res.json()
        print(f"Статус VM {vmid}: {status_info}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error getting status for VM {vmid}: {e}")
        return "Failed to get VM status", 500

    return redirect(url_for("index"))

@app.route("/health", methods=["GET"])
def healthcheck():
    return jsonify({"status": "200"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



