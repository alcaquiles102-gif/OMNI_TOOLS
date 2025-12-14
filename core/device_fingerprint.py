from rich.panel import Panel
from rich.console import Console

console = Console()

DEVICE_PROFILES = {
    "Samsung Galaxy A34": "🟢 Conectado: Dispositivo Principal de Aquiles",
    "Lenovo Tab M9": "💻 Conectado: Cyberdeck (SIMPLEMENTE INCREIBLE)",
    "Senwa S50": "🎵 Conectado: Proyecto S50 (Celular de Respaldo/DAP)",
    "Infinix NOTE 40 Pro": "💀 Conectado: ¿Revivieron los muertos? Intentando enlace..."
}

def fingerprint(adb):
    model = adb.shell("getprop ro.product.model")
    name = adb.shell("getprop ro.product.device")

    banner = DEVICE_PROFILES.get(
        model,
        f"⚠️ Dispositivo Genérico Detectado: {model}"
    )

    root = False
    try:
        adb.shell("su -c id")
        root = True
    except:
        pass

    if "Lenovo" in model and root:
        banner += " [Root Detected]"

    console.print(
        Panel.fit(
            f"[bold cyan]{banner}[/bold cyan]\n\n"
            f"[white]Modelo:[/white] {model}\n"
            f"[white]Device:[/white] {name}",
            border_style="bright_magenta"
        )
    )

    return model, name, root
