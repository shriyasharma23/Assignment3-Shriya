"""
host_info.py — Base/Parent class for hardware info.

Defines the abstract blueprint that LinuxHost and WindowsHost must follow.
All common attributes (hostname, memory, etc.) and the display method live here.
"""

from abc import ABC, abstractmethod  # ABC = Abstract Base Class
import json


class HostInfo(ABC):
    """
    Abstract parent class representing a generic host/machine.

    Child classes (LinuxHost, WindowsHost) MUST implement get_hardware_info().
    This class handles the common attributes and display logic.
    """

    def __init__(self):
        # These attributes will be filled in by each child class
        self.hostname  = None   # Machine's network name
        self.memory    = None   # Total RAM (e.g. "8 GB")
        self.cpu       = None   # Processor name/speed
        self.ip        = None   # IP address
        self.disk_size = None   # Total disk storage

    @abstractmethod
    def get_hardware_info(self):
        """
        Abstract method — MUST be implemented by every child class.
        Each OS (Linux/Windows) queries hardware differently, so each
        child class writes its own version of this method.
        """
        pass  # No body here — child classes provide the implementation

    def display_hardware_info(self):
        """
        Displays the collected hardware info as formatted JSON.
        This method is common to all hosts, so it lives in the parent class.
        """
        info = {
            "hostname"  : self.hostname,
            "ip"        : self.ip,
            "memory"    : self.memory,
            "cpu"       : self.cpu,
            "disk_size" : self.disk_size
        }
        # indent=4 makes the JSON output nicely formatted and readable
        print(json.dumps(info, indent=4))