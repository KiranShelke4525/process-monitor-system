
from rest_framework import serializers
from .models import ApiKey, SystemInfo, ProcessInfo

class ProcessInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessInfo
        fields = ["id","name","pid","ppid","cpu_percent","memory_mb"]

class SystemInfoSerializer(serializers.ModelSerializer):
    processes = ProcessInfoSerializer(many=True)

    class Meta:
        model = SystemInfo
        fields = [
            "id","hostname","os","os_version","processor","num_cpus","num_threads",
            "ram_total_gb","ram_used_gb","ram_available_gb",
            "disk_total_gb","disk_used_gb","disk_free_gb",
            "timestamp","processes"
        ]

    def create(self, validated_data):
        procs = validated_data.pop("processes", [])
        system = SystemInfo.objects.create(**validated_data)
        proc_objs = [ProcessInfo(system=system,
                                 name=p.get("name",""),
                                 pid=int(p.get("pid",0)),
                                 ppid=int(p.get("ppid",0)),
                                 cpu_percent=float(p.get("cpu_percent",0.0)),
                                 memory_mb=float(p.get("memory_mb",0.0))) for p in procs]
        ProcessInfo.objects.bulk_create(proc_objs)
        return system
