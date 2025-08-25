# backend/backend_app/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import ApiKey, SystemInfo, ProcessInfo
import json
from django.shortcuts import render

@csrf_exempt
def ingest_agent_data(request):
    """
    Endpoint: POST /agent/ingest/
    Stores system + process data sent by agents.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

   
    api_key = request.headers.get("X-API-KEY")
    if not ApiKey.objects.filter(key=api_key).exists():
        return JsonResponse({"error": "Unauthorized"}, status=401)


    system = SystemInfo.objects.create(
        hostname=data.get("hostname"),
        os=data.get("os"),
        os_version=data.get("os_version"),
        processor=data.get("processor"),
        num_cpus=data.get("num_cpus", 1),
        num_threads=data.get("num_threads", 1),
        ram_total_gb=data.get("ram_total_gb", 0.0),
        ram_used_gb=data.get("ram_used_gb", 0.0),
        ram_available_gb=data.get("ram_available_gb", 0.0),
        disk_total_gb=data.get("disk_total_gb", 0.0),
        disk_used_gb=data.get("disk_used_gb", 0.0),
        disk_free_gb=data.get("disk_free_gb", 0.0),
        timestamp=timezone.now(),
    )


    processes = data.get("processes", [])
    for proc in processes:
        ProcessInfo.objects.create(
            system=system,
            name=proc.get("name"),
            pid=proc.get("pid"),
            ppid=proc.get("ppid", 0),
            cpu_percent=proc.get("cpu_percent", 0.0),
            memory_mb=proc.get("memory_mb", 0.0),
        )

    return JsonResponse({"status": "success", "system_id": system.id})


def latest_systems(request):
    """
    Endpoint: GET /agent/latest/
    Returns latest system info from all agents.
    """
    latest = SystemInfo.objects.order_by("-timestamp")[:10] 
    data = [
        {
            "id": s.id,
            "hostname": s.hostname,
            "os": s.os,
            "os_version": s.os_version,
            "processor": s.processor,
            "num_cpus": s.num_cpus,
            "num_threads": s.num_threads,
            "ram_total_gb": s.ram_total_gb,
            "ram_used_gb": s.ram_used_gb,
            "ram_available_gb": s.ram_available_gb,
            "disk_total_gb": s.disk_total_gb,
            "disk_used_gb": s.disk_used_gb,
            "disk_free_gb": s.disk_free_gb,
            "timestamp": s.timestamp,
        }
        for s in latest
    ]
    return JsonResponse(data, safe=False)


def system_detail(request, system_id):
    try:
        system = SystemInfo.objects.get(id=system_id)
    except SystemInfo.DoesNotExist:
        return JsonResponse({"error": "System not found"}, status=404)

    processes = [
        {
            "pid": p.pid,
            "ppid": p.ppid,
            "name": p.name,
            "cpu_percent": p.cpu_percent,
            "memory_mb": p.memory_mb,
        }
        for p in system.processes.all()
    ]

    return JsonResponse({
        "id": system.id,
        "hostname": system.hostname,
        "os": system.os,
        "os_version": system.os_version,
        "processor": system.processor,
        "num_cpus": system.num_cpus,
        "num_threads": system.num_threads,
        "ram_total_gb": system.ram_total_gb,
        "ram_used_gb": system.ram_used_gb,
        "ram_available_gb": system.ram_available_gb,
        "disk_total_gb": system.disk_total_gb,
        "disk_used_gb": system.disk_used_gb,
        "disk_free_gb": system.disk_free_gb,
        "timestamp": system.timestamp,
        "processes": processes,
    })


def monitor(request):
    return render(request, "backend_app/index.html")