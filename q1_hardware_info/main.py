"""
main.py — Entry point for the Hardware Info program.

Detects the current OS automatically and creates the right host object.
Then fetches and displays hardware information in JSON format.
"""

import platform     # Standard library to detect the OS
from linux_host   import LinuxHost
from windows_host import WindowsHost


def main():
    # Detect the operating system this script is running on
    os_type = platform.system()   # Returns "Linux", "Windows", or "Darwin"

    print(f"Detected OS: {os_type}")
    print("Fetching hardware info...\n")

    # Instantiate the correct child class based on OS
    if os_type == "Linux":
        host = LinuxHost()
    elif os_type == "Windows":
        host = WindowsHost()
    else:
        # macOS or other unsupported OS
        raise Exception(
            f"Unsupported OS: '{os_type}'. "
            "This program only supports Linux and Windows."
        )

    # Step 1: Collect hardware info (fills in the attributes)
    host.get_hardware_info()

    # Step 2: Display the info as JSON
    host.display_hardware_info()


if __name__ == "__main__":
    main()