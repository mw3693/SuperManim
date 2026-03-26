import shutil
from config.constants import MIN_ABS_DISK_SPACE_GB

def has_minimum_disk_space(path: str, min_gb: float = MIN_ABS_DISK_SPACE_GB) -> bool:
    """
    Check if the disk that contains the given path has enough free space.

    This function verifies that the disk has at least the minimum required
    amount of free space before creating a new project. If the available
    space is lower than the required minimum, the function shows a clear
    message and returns False.

    Parameters
    ----------
    path : str
        The project path where the new project directory will be created.
        The disk that contains this path will be checked.

    min_gb : float, optional
        The minimum required free space in gigabytes. Default is 3.0 GB.

    Returns
    -------
    bool
        True if the disk has enough free space.
        False if the disk does not have enough free space or an error occurs.
    """
    try:
        # Get disk usage statistics
        disk_usage = shutil.disk_usage(path)
        free_bytes = disk_usage.free

        # Convert free space from bytes to gigabytes
        free_gb = free_bytes / (1024 ** 3)

        # Compare free space with minimum requirement
        if free_gb >= min_gb:
            return True
        else:
            print(
                f"[Error] Not enough disk space to create the project.\n"
                f"  Path     : {path}\n"
                f"  Required : {min_gb:.2f} GB\n"
                f"  Available: {free_gb:.2f} GB\n"
                f"  Please free up space or choose a different location."
            )
            return False

    except FileNotFoundError as e:
        print(
            f"[Error] The specified path does not exist:\n"
            f"  Path : {path}\n"
            f"  Details: {e}"
        )
        return False
    except PermissionError as e:
        print(
            f"[Error] Permission denied while checking disk space:\n"
            f"  Path : {path}\n"
            f"  Details: {e}\n"
            f"  Please ensure you have access to this location."
        )
        return False
    except OSError as e:
        print(
            f"[Error] OS error occurred while checking disk space:\n"
            f"  Path : {path}\n"
            f"  Details: {e}\n"
            f"  This may be due to a disconnected or unmounted disk."
        )
        return False
