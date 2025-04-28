# Spot VM Manager for Proxmox

This project provides a simple web interface to:
- Create Spot VMs from a Proxmox template
- Automatically start and stop VMs based on a schedule
- Manually start, stop, or delete VMs
- View live status of each VM

---

## Technologies

- Python 3.11+
- Flask
- Proxmoxer (Proxmox API client)
- HTML (Jinja2 templates)

---

## Installation

1. Clone the repository:

```bash
git clone <repo-url>
cd Spot-proxmox
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure your `config.py`:

```python
PROXMOX_HOST = "192.168.77.2"
PROXMOX_USER = "root@pam"
PROXMOX_PASS = "your_password"
PROXMOX_NODE = "node_name"
```

5. Create an empty `instances.json` file:

```json
{}
```

---

## Running the App

```bash
source venv/bin/activate
python app.py
```

The application will be available at:  
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## Features

- Create new Spot VMs from templates
- Set working schedule (start_time, end_time) for each VM
- Automatic start/stop based on schedule
- Live VM status fetching via Proxmox API
- Background thread checking and managing VM states

---

## Project Structure

```
Spot-proxmox/
├── app.py                # Flask web server
├── templates/index.html  # Main HTML page
├── services/
│   └── proxmox.py        # Proxmox API logic
├── utils/
│   └── storage.py        # JSON load/save helpers
├── config.py             # Proxmox connection settings
├── instances.json        # Database of Spot VMs
├── requirements.txt      # Python dependencies
```

---

## Future Plans

- [ ] Auto-delete expired Spot VMs
- [ ] Telegram/email notifications on errors
- [ ] Search and filter VMs by status
- [ ] Responsive web interface

---

# Let's automate Proxmox with Spot-VMs! 🚀

