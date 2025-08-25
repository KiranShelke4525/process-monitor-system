from django.db import models

class ApiKey(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.name} - {self.key[:8]}..."

class SystemInfo(models.Model):
    hostname = models.CharField(max_length=255)
    os = models.CharField(max_length=255, blank=True, null=True)
    os_version = models.CharField(max_length=255, blank=True, null=True)
    processor = models.CharField(max_length=255, blank=True, null=True)
    num_cpus = models.IntegerField(default=1)
    num_threads = models.IntegerField(default=1)
    ram_total_gb = models.FloatField(default=0.0)
    ram_used_gb = models.FloatField(default=0.0)
    ram_available_gb = models.FloatField(default=0.0)
    disk_total_gb = models.FloatField(default=0.0)
    disk_used_gb = models.FloatField(default=0.0)
    disk_free_gb = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.hostname} @ {self.timestamp}"

class ProcessInfo(models.Model):
    system = models.ForeignKey(SystemInfo, on_delete=models.CASCADE, related_name="processes")
    name = models.CharField(max_length=255, blank=True, null=True)
    pid = models.IntegerField()
    ppid = models.IntegerField(default=0)
    cpu_percent = models.FloatField(default=0.0)
    memory_mb = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.name} ({self.pid})"
