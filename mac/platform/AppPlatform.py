from enum import Enum
import subprocess

class PlatformType(Enum):
    ANDROID = "android"
    IOS = "ios"

def is_android_running():
    try:
        result = subprocess.check_output(["adb", "devices"]).decode()
        return "emulator" in result
    except:
        return False

def is_ios_running():
    try:
        result = subprocess.check_output(["xcrun", "simctl", "list", "devices", "booted"]).decode()
        return "Booted" in result
    except:
        return False

def detect_available_platforms():
    platforms = []

    android = is_android_running()
    ios = is_ios_running()
    print(f"[DEBUG] Android 실행 여부: {android}")
    print(f"[DEBUG] iOS 실행 여부: {ios}")

    if android:
        platforms.append(PlatformType.ANDROID)

    if ios:
        platforms.append(PlatformType.IOS)

    print(f"[DEBUG] 감지된 플랫폼: {platforms}")
    return platforms
