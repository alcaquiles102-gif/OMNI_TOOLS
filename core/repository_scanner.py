from pathlib import Path
from rich.progress import track
from rich.console import Console
import os

console = Console()

VALID_EXTENSIONS = (".apk", ".img", ".zip")

def detect_base_path():
    linux_path = Path("/mnt/DATOS")
    if linux_path.exists():
        return linux_path

    for letter in "DEFGHI":
        win_path = Path(f"{letter}:/")
        if win_path.exists():
            return win_path

    raise FileNotFoundError("No se encontró la partición compartida")

def scan_repository(base_path: Path):
    files = []
    for path in track(base_path.rglob("*"), description="Escaneando repositorio..."):
        if path.suffix.lower() in VALID_EXTENSIONS:
            files.append(path)
    return files
