"""
windows_host.py — Windows-specific hardware info collector.

Inherits from HostInfo and implements get_hardware_info()
using Windows commands like 'systeminfo' and 'wmic'.
"""

import subprocess   # To run Windows shell commands
import socket       # For hostname and IP
from host_info import HostInfo


class WindowsHost(HostInfo):
    """
    Child class for Windows machines.
    Uses 'systeminfo' and 'wmic' commands to gather hardware details.
    """

    def _run_command(self, command):
        """
        Helper method to safely run a Windows command and return output.
        Returns 'N/A' if the command fails.
        """
        try:
            result = subprocess.check_output(
                command, shell=True, stderr=subprocess.DEVNULL
            )
            return result.decode("utf-8", errors="ignore").strip()
        except Exception:
            return "N/A"

    def get_hardware_info(self):
        """
        Implements the abstract method from HostInfo.
        Collects all hardware details using Windows-specific commands.
        """

        # --- Hostname ---
        self.hostname = socket.gethostname()

        # --- IP Address ---
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            self.ip = s.getsockname()[0]
            s.close()
        except Exception:
            self.ip = socket.gethostbyname(self.hostname)

        # --- Memory ---
        # wmic gives exact bytes; convert to GB for readability
        mem_raw = self._run_command(
            'wmic ComputerSystem get TotalPhysicalMemory /value'
        )
        for line in mem_raw.splitlines():
            if "TotalPhysicalMemory=" in line:
                try:
                    bytes_val = int(line.split("=")[1].strip())
                    # Convert bytes to GB (1 GB = 1024^3 bytes)
                    self.memory = f"{bytes_val / (1024**3):.1f} GB"
                except Exception:
                    self.memory = "N/A"
                break

        # --- CPU ---
        # wmic cpu get Name returns the processor name
        cpu_raw = self._run_command('wmic cpu get Name /value')
        for line in cpu_raw.splitlines():
            if "Name=" in line:
                self.cpu = line.split("=")[1].strip()
                break

        # --- Disk Size ---
        # wmic logicaldisk gets info on all drives
        # We sum all drive sizes and convert to GB
        disk_raw = self._run_command('wmic logicaldisk get Size /value')
        total_bytes = 0
        for line in disk_raw.splitlines():
            if "Size=" in line:
                try:
                    val = line.split("=")[1].strip()
                    if val:
                        total_bytes += int(val)
                except Exception:
                    pass
        self.disk_size = f"{total_bytes / (1024**3):.1f} GB" if total_bytes > 0 else "N/A"