import psutil
import platform
import socket
import requests
import time
import json

API_URL = "http://127.0.0.1:8000/api/agent/ingest/"
API_KEY = "super-secret-key-123"  # Replace with actual key from Django DB

def get_system_info():
    # Handle disk usage for different OS
    try:
        if platform.system() == "Windows":
            disk_path = "C:\\"
        else:
            disk_path = "/"
        disk = psutil.disk_usage(disk_path)
    except Exception:
        # Fallback if disk access fails
        disk = type('obj', (object,), {'total': 0, 'used': 0, 'free': 0})

    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.version(),
        "processor": platform.processor(),
        "num_cpus": psutil.cpu_count(logical=False) or 1,
        "num_threads": psutil.cpu_count(logical=True) or 1,
        "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "ram_used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
        "ram_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
        "disk_total_gb": round(disk.total / (1024**3), 2),
        "disk_used_gb": round(disk.used / (1024**3), 2),
        "disk_free_gb": round(disk.free / (1024**3), 2),
    }

def get_processes_info():
    processes = []
    
    # First pass to initialize cpu_percent
    for proc in psutil.process_iter(['pid']):
        try:
            proc.cpu_percent(interval=None)
        except:
            pass
    
    # Small delay to get accurate CPU readings
    time.sleep(0.1)
    
    for proc in psutil.process_iter(['pid', 'ppid', 'name', 'cpu_percent', 'memory_info']):
        try:
            proc_info = proc.info
            mem_mb = proc_info['memory_info'].rss / (1024 * 1024) if proc_info.get('memory_info') else 0
            
            processes.append({
                "pid": proc_info.get('pid', 0),
                "ppid": proc_info.get('ppid', 0),
                "name": proc_info.get('name', 'Unknown'),
                "cpu_percent": proc_info.get('cpu_percent', 0.0) or 0.0,
                "memory_mb": round(mem_mb, 2)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    return processes

def send_data():
    print(" Collecting system data...")
    
    # Get system and process data
    data = get_system_info()
    data["processes"] = get_processes_info()
    
    print(f" Collected {len(data['processes'])} processes from {data['hostname']}")
    
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": API_KEY
    }
    
    try:
        print(f"Sending data to {API_URL}")
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))
        
        if response.status_code in (200, 201):
            result = response.json()
            print(f"Data sent successfully! System ID: {result.get('system_id', 'unknown')}")
        else:
            print(f" Failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Connection failed! Is your Django server running at http://127.0.0.1:8000?")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f" Unexpected error: {e}")

if __name__ == "__main__":
    print("Process Monitor Agent Started")
    print(f" Backend URL: {API_URL}")
    print(f" API Key: {API_KEY[:10]}...")
    print(" Press Ctrl+C to stop\n")
    
    try:
        while True:
            send_data()
            print("Waiting 10 seconds...\n")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nAgent stopped by user")
    except Exception as e:
        print(f"\n Agent crashed: {e}")