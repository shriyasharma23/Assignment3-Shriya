"""
linux_host.py — Linux-specific hardware info collector.

Inherits from HostInfo and implements get_hardware_info()
using standard Linux shell commands.
"""

import subprocess   # To run shell commands from Python
import socket       # To get hostname and IP address
from host_info import HostInfo


class LinuxHost(HostInfo):
    """
    Child class for Linux machines.
    Uses Linux commands like 'free', 'lscpu', 'df' to get hardware info.
    """

    def _run_command(self, command):
        """
        Helper method to run a shell command and return its output as a string.
        Returns 'N/A' if the command fails (so the program doesn't crash).
        """
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
            return result.decode("utf-8").strip()
        except Exception:
            return "N/A"

    def get_hardware_info(self):
        """
        Implements the abstract method from HostInfo.
        Queries all hardware details using Linux commands and stores them.
        """

        # --- Hostname ---
        # socket.gethostname() returns the machine's name on the network
        self.hostname = socket.gethostname()

        # --- IP Address ---
        try:
            # Connect to an external address to find which local IP is used
            # We don't actually send data — just use it to detect the IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            self.ip = s.getsockname()[0]
            s.close()
        except Exception:
            self.ip = socket.gethostbyname(self.hostname)

        # --- Memory ---
        # 'free -h' shows RAM in human-readable form (e.g. "7.7Gi")
        # awk picks the total memory from the "Mem:" row
        self.memory = self._run_command("free -h | awk '/^Mem:/{print $2}'")

        # --- CPU ---
        # 'lscpu' lists CPU details; grep finds the model name line
        # awk -F: splits on colon and prints the second part (the value)
        cpu_raw = self._run_command("lscpu | grep 'Model name' | awk -F':' '{print $2}'")
        self.cpu = cpu_raw.strip() if cpu_raw != "N/A" else self._run_command(
            "cat /proc/cpuinfo | grep 'model name' | head -1 | awk -F':' '{print $2}'"
        )

        # --- Disk Size ---
        # 'df -h --total' shows disk usage; tail -1 gets the "total" row
        # awk '{print $2}' gets the total size column
        self.disk_size = self._run_command("df -h --total | tail -1 | awk '{print $2}'")