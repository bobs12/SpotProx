
from proxmoxer import ProxmoxAPI
from config import PROXMOX_HOST, PROXMOX_USER, PROXMOX_PASS, PROXMOX_NODE
from utils.storage import load_instances, save_instances
import uuid
from datetime import datetime, timedelta, timezone
import json
import time


proxmox = ProxmoxAPI(PROXMOX_HOST, user=PROXMOX_USER, password=PROXMOX_PASS, verify_ssl=False)

def get_proxmox():
    return proxmox


def clone_vm(source_vm_id, target_vm_id, target_node):
    """
    Clone a VM from source_vm_id to target_vm_id on the specified target_node.
    """
    try:
        proxmox.nodes(PROXMOX_NODE).qemu(source_vm_id).clone.create(
            newid=target_vm_id,
            full=True,
            name=f"cloned-{target_vm_id}",
            target=target_node
        )
        print(f"Cloning VM {source_vm_id} to {target_vm_id} on {target_node}...")
    except Exception as e:
        print(f"Error cloning VM: {e}")

def list_vms():
    proxmox = get_proxmox()
    try:
        return proxmox.nodes(PROXMOX_NODE).qemu.get()
    except Exception as e:
        print(f"Error listing VMs: {e}")
        return []
    
def node_list():
    """
    Get a list of nodes in the Proxmox cluster.
    """
    try:
        nodes = proxmox.nodes.get()
        return [node['node'] for node in nodes]
    except Exception as e:
        print(f"Error getting node list: {e}")
        return []
    
def create_vm(vm_id, vm_name, vm_template):
    """
    Create a new VM from a template.
    """
    try:
        proxmox.nodes(PROXMOX_NODE).qemu.create(
            vmid=vm_id,
            name=vm_name,
            clone=vm_template,
            full=True
        )
        print(f"Creating VM {vm_name} from template {vm_template}...")
    except Exception as e:
        print(f"Error creating VM: {e}")

def delete_vm(vm_id):
    proxmox = get_proxmox()

    try:
        # 1. Видалення VM з Proxmox
        proxmox.nodes(PROXMOX_NODE).qemu(vm_id).delete()
        print(f"Deleting VM {vm_id}...")

        # 2. Видалення з JSON
        with open("instances.json", 'r') as f:
            data = json.load(f)

        vmid_str = str(vm_id)
        if vmid_str in data:
            del data[vmid_str]
            print(f"Deleted VM {vmid_str} from JSON")

            with open("instances.json", 'w') as f:
                json.dump(data, f, indent=2)
        else:
            print(f"⚠️ VM ID {vmid_str} not found in instances.json")

    except Exception as e:
        print(f"Error deleting VM: {e}")

def spot_vm(vm_id: int, vm_name: str, vm_template: int, duration: int, start_time: str, end_time: str):
    proxmox = get_proxmox()
    
    
    try:
        proxmox.nodes(PROXMOX_NODE).qemu(vm_template).clone.create(
            newid=vm_name,
            name=vm_id,
            #full=True
        )
    except Exception as e:
        # Handle the error
        print(f"Error creating spot instance: {e}")
        return None
    instance = load_instances()
    instance[vm_id] = {
        "name": vm_name,
        "template": vm_template,
        "duration": duration,
        "start_time": start_time,
        "end_time": end_time,
    }

    config = instance.get(vm_id)
    save_instances(instance)

    return vm_id

def manage_power_from_schedule(json_path, node_name):
    proxmox = get_proxmox()

    while True:

        now = datetime.now().time()

        try:
            with open(json_path, 'r') as f:
                schedules = json.load(f)
        except Exception as e:
            print(f"❌ Error reading schedule file: {e}")
            time.sleep(30)
            continue

        for key, config in schedules.items():
            try:
                vmid = int(config.get("name"))  # ← name = vmid у тебе

                start_str = config.get("start_time")
                end_str = config.get("end_time")
                if not start_str or not end_str:
                    print(f"⚠️ Skipping {key}: no start/end time")
                    continue

                start = datetime.strptime(start_str, "%H:%M").time()
                end = datetime.strptime(end_str, "%H:%M").time()

                # отримуємо статус ВМ
                status = proxmox.nodes(node_name).qemu(vmid).status.current.get()["status"]

                if start <= now <= end:
                    if status == "stopped":
                        print(f"[▶️] Starting VM {vmid} ({key})")
                        proxmox.nodes(node_name).qemu(vmid).status.start.post()
                else:
                    if status == "running":
                        print(f"[⏹] Stopping VM {vmid} ({key})")
                        proxmox.nodes(node_name).qemu(vmid).status.stop.post()

            except Exception as e:
                print(f"⚠️ Failed to manage VM from {key}: {e}")
        
        time.sleep(30)

def load_instances():
    """
    Load instances from the JSON file.
    """
    try:
        with open("instances.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("⚠️ Error decoding JSON file.")
        return {}
    except Exception as e:
        print(f"⚠️ Error loading instances: {e}")
        return {}
    
def get_instances_with_live_status():
    proxmox = get_proxmox()

    with open("instances.json", "r") as f:
        data = json.load(f)

    instances = []

    for vmid_str, info in data.items():
        vmid = int(vmid_str)
        instance = dict(info)
        instance["vmid"] = vmid_str

        try:
            status_info = proxmox.nodes(PROXMOX_NODE).qemu(vmid).status.current.get()
            instance["status"] = status_info.get("status", "невідомо")
        except Exception as e:
            instance["status"] = f"⚠️ {e}"

        instances.append(instance)
    time.sleep(5)
    return instances
