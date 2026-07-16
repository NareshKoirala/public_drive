import subprocess
import json
from osFunc import createDir


def findDrives():
    drives = []

    r = subprocess.run(["lsblk", "-Jo", "NAME,PATH"], capture_output=True, text=True)
    d = json.loads(r.stdout)

    for dr in d.get("blockdevices"):
        if dr.get("name").startswith("sd"):
            drives.append(dr.get("children"))

    return drives


def mountDrives(root):
    drs = findDrives()

    for dr in drs:
         pass
