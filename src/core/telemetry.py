import time
import json
import os

class EngineTelemetry:
    def __init__(self, engine_name):
        self.engine_name = engine_name
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self, total_keys):
        self.end_time = time.perf_counter()
        duration = self.end_time - self.start_time
        keys_per_second = total_keys / duration if duration > 0 else 0
        metrics = {"engine": self.engine_name, "duration_seconds": round(duration, 4), "total_keys_audited": total_keys, "performance_keys_sec": round(keys_per_second, 2), "status": "CERTIFIED_AUDIT"}
        return metrics

    def export_to_json(self, metrics, filepath="interface/telemetry.json"):
        try:
            data = []
            if os.path.exists(filepath):
                with open(filepath, "r") as f: data = json.load(f)
            data.append(metrics)
            with open(filepath, "w") as f: json.dump(data, f, indent=4)
        except Exception: pass
