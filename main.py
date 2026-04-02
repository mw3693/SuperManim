import sys

MIN_PYTHON = (3, 10)

if sys.version_info < MIN_PYTHON:
    # Print a clear error message to the user
    print(
        f"\033[91m[ERROR]\033[0m SuperManim requires Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or higher. "
        f"Current version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    # Exit the program with status code 1 to indicate failure
    sys.exit(1)


try:
    import manim

except ImportError:
    print("\033[91m[ERROR]\033[0m Manim is NOT installed. Run: pip install manim")
    sys.exit(1)

try:
    import ffmpeg

except ImportError:
    print("\033[91m[ERROR]\033[0m ffmpeg-python is NOT installed. Run: pip install ffmpeg-python")
    sys.exit(1)

