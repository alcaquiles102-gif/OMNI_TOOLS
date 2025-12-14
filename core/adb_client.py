import subprocess
from typing import List

class ADBClient:
    def __init__(self, adb_path="adb"):
        self.adb = adb_path

    def _run(self, args: List[str], timeout=10) -> str:
        try:
            result = subprocess.run(
                [self.adb] + args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
                text=True
            )
            if result.returncode != 0:
                raise RuntimeError(result.stderr.strip())
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            raise RuntimeError("ADB no responde (timeout)")

    def shell(self, cmd: str) -> str:
        return self._run(["shell", cmd])

    def devices(self):
        output = self._run(["devices"])
        lines = output.splitlines()[1:]  # saltar encabezado

        devices = []
        for line in lines:
            if not line.strip():
                continue
        serial, status = line.split()
        devices.append((serial, status))

        return devices

    def install(self, apk_path: str):
        return self._run(["install", apk_path])

    def uninstall(self, package: str):
        return self._run(["shell", "pm", "uninstall", "--user", "0", package])
