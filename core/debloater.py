import json
from datetime import datetime
from rich.console import Console
from questionary import checkbox, confirm

from data.package_aliases import ALIASES
from data.safe_packages import SAFE_PACKAGES

console = Console()

def get_packages(adb):
    raw = adb.shell("pm list packages")
    return [p.replace("package:", "") for p in raw.splitlines()]

def debloat(adb):
    packages = get_packages(adb)

    choices = []
    for pkg in packages:
        label = ALIASES.get(pkg, pkg)
        tag = "[SAFE]" if pkg in SAFE_PACKAGES else "[?]"
        choices.append(f"{tag} {label} ({pkg})")

    selected = checkbox(
        "Selecciona paquetes a desinstalar:",
        choices=choices
    ).ask()

    if not selected:
        console.print("[yellow]Nada seleccionado. Abortando.[/yellow]")
        return

    if not confirm("¿Confirmar desinstalación?").ask():
        return

    backup = {
        "timestamp": datetime.now().isoformat(),
        "packages": selected
    }

    backup_path = f"backups/debloat_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(backup_path, "w") as f:
        json.dump(backup, f, indent=2)

    for entry in selected:
        pkg = entry.split("(")[-1].replace(")", "")
        adb.uninstall(pkg)

    console.print(f"[green]Respaldo generado:[/green] {backup_path}")
