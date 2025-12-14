from rich.console import Console

console = Console()

def check_bootloader(adb):
    try:
        locked = adb.shell("getprop ro.boot.flash.locked")
        return locked
    except:
        return "UNKNOWN"

def dump_partitions(adb):
    return adb.shell("cat /proc/partitions")
