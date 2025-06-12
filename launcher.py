import subprocess

def launch_app_with_rez(rez_package: str, command: str):
    full_command = f"rez env {rez_package} -- {command}"
    subprocess.Popen(full_command, shell=True)
