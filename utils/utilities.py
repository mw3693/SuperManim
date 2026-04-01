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




def calculate_required_space_bytes(
    video_bitrate_mbps: float,
    total_video_duration_sec: int,
    width: int = 3840,
    height: int = 2160,
    fps: int = 60,
    audio_bitrate_kbps: int = DEFAULT_AUDIO_BITRATE_KBPS,
    intermediate_compression_ratio: float = INTERMEDIATE_COMPRESSION_RATIO,
    safety_margin: float = SAFETY_MARGIN,
    min_abs_gb: float = MIN_ABS_DISK_SPACE_GB,
) -> int:
    """
    Estimate the minimum disk space (in bytes) required for a project.

    The estimate accounts for:
    * Final encoded video size
    * Encoded audio size
    * Intermediate (uncompressed then partially compressed) render frames
    * A configurable safety margin
    * An absolute floor so tiny projects are never under-estimated

    Parameters
    ----------
    video_bitrate_mbps:
        Target video bitrate in megabits per second.
    total_video_duration_sec:
        Total project duration in seconds.
    width, height:
        Output resolution in pixels.  Defaults to 4K.
    fps:
        Frames per second.
    audio_bitrate_kbps:
        Audio bitrate used for the audio size estimate.
    intermediate_compression_ratio:
        Fraction of raw frame size kept after intermediate compression.
    safety_margin:
        Multiplier applied to the total estimate (e.g. 1.3 = +30 %).
    min_abs_gb:
        Hard floor in gigabytes — the return value will never be less than this.

    Returns
    -------
    int
        Required disk space in bytes.
    """
    # 1. Final video size  (Mbps × seconds) / 8  →  megabytes
    video_size_mb: float = (video_bitrate_mbps * total_video_duration_sec) / 8

    # 2. Audio size  (Kbps × seconds) / 8 / 1024  →  megabytes
    audio_size_mb: float = (audio_bitrate_kbps * total_video_duration_sec) / (8 * 1024)

    # 3. Intermediate frames — raw pixel size × compression ratio
    raw_frame_size_mb: float = (width * height * 3) / (1024 ** 2)
    num_frames: int = fps * total_video_duration_sec
    intermediate_size_mb: float = raw_frame_size_mb * num_frames * intermediate_compression_ratio

    # 4. Total with safety buffer
    total_mb: float = (video_size_mb + audio_size_mb + intermediate_size_mb) * safety_margin

    # 5. Convert MB → bytes and enforce absolute floor
    required_bytes: int = ceil(total_mb * 1024 ** 2)
    min_bytes: int = ceil(min_abs_gb * 1024 ** 3)
    return max(required_bytes, min_bytes)


def has_enough_disk_space(
    path: str,
    video_bitrate_mbps: float,
    total_video_duration_sec: int,
    width: int = 3840,
    height: int = 2160,
    fps: int = 60,
    audio_bitrate_kbps: int = DEFAULT_AUDIO_BITRATE_KBPS,
) -> bool:
    """
    Return ``True`` if the filesystem at *path* has enough free space to start
    the project safely; ``False`` otherwise.

    Prints a human-readable error message when space is insufficient or when
    the disk cannot be queried.

    Parameters
    ----------
    path:
        Directory (or any path on the target volume) to inspect.
    video_bitrate_mbps, total_video_duration_sec, width, height, fps,
    audio_bitrate_kbps:
        Passed through to :func:`calculate_required_space_bytes`.

    Returns
    -------
    bool
    """
    import shutil  # Imported locally; shutil is stdlib — no overhead concern.

    required_bytes = calculate_required_space_bytes(
        video_bitrate_mbps,
        total_video_duration_sec,
        width,
        height,
        fps,
        audio_bitrate_kbps,
    )

    try:
        _, _, free_bytes = shutil.disk_usage(path)
        if free_bytes < required_bytes:
            required_gb = round(required_bytes / (1024 ** 3), 2)
            free_gb     = round(free_bytes     / (1024 ** 3), 2)
            print("Error: Insufficient disk space to start this project.")
            print(
                f"Required (with margin): {required_gb} GB  |  "
                f"Available: {free_gb} GB"
            )
            return False
        return True
    except (FileNotFoundError, PermissionError, OSError) as exc:
        print(f"Error: Could not verify disk space at '{path}'. Details: {exc}")
        return False


