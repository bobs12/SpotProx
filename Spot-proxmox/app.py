
import threading
from flask import Flask, render_template, request, redirect, url_for
from services.proxmox import spot_vm,load_instances, manage_power_from_schedule, delete_vm, load_instances, get_instances_with_live_status

app = Flask(__name__)

threading.Thread(
    target=manage_power_from_schedule,
    args=("instances.json", "node3"), 
    daemon=True
).start()

# threading.Thread(
#     target=get_instances_with_live_status,
#     args=(), 
#     daemon=True
# ).start()

@app.route("/")
def index():
    raw_data = load_instances()
    instances = []
    for vm_id, data in raw_data.items():
        instance = {
            "id": vm_id,
            "name": data["name"],
            "template": data["template"],
            "duration": data["duration"],
            "start_time": data["start_time"],
            "end_time": data["end_time"]
        }
        instances.append(instance)
        instances = get_instances_with_live_status()
    return render_template("darktheme.html", instances=instances)
   
@app.route("/create", methods=["POST"])
def create():
    name = request.form["name"]
    #id = request.form["id"]
    template = int(request.form["template"])
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]
    spot_vm(vm_id=name,vm_name=name,vm_template=template, start_time=start_time, end_time=end_time,duration=1)
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
    vm_status()
    return redirect(url_for("index"))



if __name__ == "__main__":
    app.run(debug=True)
    vm_status()



