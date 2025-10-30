import pytest
import subprocess
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test_app.platform.openApp import *
from test_app.platform.AppPlatform import *
from test_app.common.common_function import *
from test_app.app import *
from enum import Enum


# iOS 앱 삭제 함수
def uninstall_ios_app(simulator_name: str, bundle_id: str):
    try:
        output = subprocess.check_output(["xcrun", "simctl", "list", "devices", "--json"], text=True)
        devices = json.loads(output)["devices"]

        for runtimes in devices.values():
            for device in runtimes:
                if device["name"] == simulator_name and device["state"] == "Booted":
                    udid = device["udid"]
                    subprocess.run(["xcrun", "simctl", "uninstall", udid, bundle_id], check=True)
                    print(f"✅ iOS 앱 삭제 완료: {bundle_id} (on {simulator_name})")
                    return
        print(f"⚠️ 실행 중인 iOS 시뮬레이터 '{simulator_name}'을 찾을 수 없음")
    except Exception as e:
        print(f"❌ iOS 앱 삭제 실패: {e}")

# Android 앱 삭제 함수
def uninstall_android_app(package_name: str):
    try:
        subprocess.run(["adb", "uninstall", package_name], check=True)
        print(f"✅ Android 앱 삭제 완료: {package_name}")
    except Exception as e:
        print(f"❌ Android 앱 삭제 실패: {e}")


@pytest.fixture(params=detect_available_platforms(), scope="function")
def driver(request):
    platform = request.param
    driver_instance = None
    package_or_bundle_id = None

    if platform == PlatformType.ANDROID:
        driver_instance, package_or_bundle_id = open_app(app_type=AppType.STAGING, platform=PlatformType.ANDROID, device_name="emulator-5554", port=4723)
    elif platform == PlatformType.IOS:
        driver_instance, package_or_bundle_id = open_app(app_type=AppType.STAGING, platform=PlatformType.IOS, device_name="iPhone 15 Pro", port=4725)
 
    else:
        raise ValueError(f"지원하지 않는 플랫폼: {platform}")

    yield driver_instance

    try:
        driver_instance.quit()
    except Exception as e:
        print(f"driver.quit() 중 오류 발생: {e}")

    
    # # 테스트 후 앱 자동 삭제 처리
    # if platform == PlatformType.ANDROID and package_or_bundle_id:
    #     uninstall_android_app(package_or_bundle_id)
    # elif platform == PlatformType.IOS and package_or_bundle_id:
    #     uninstall_ios_app("iPhone 15 Pro", package_or_bundle_id)


@pytest.fixture(scope="session", autouse=True)
def environment():
    env = get_tailscale_status()
    print(f"\n🌐 현재 테스트 환경: {env}")
    return env


@pytest.fixture(autouse=True)
def ensure_on_book_home(driver, request):
    """
    @pytest.mark.bookhome 마커가 있고, @pytest.mark.preconditioned 마커가 없을 때에만 적용됨.
    마커 이름에 따라 book_id 결정 후, 작품홈으로 이동.
    """
    if 'bookhome' in request.node.keywords and 'preconditioned' not in request.node.keywords:
        book_id = None

        # 마커에서 어떤 book_id를 쓸지 결정
        for genre in BOOK_IDS:
            if genre in request.node.keywords:
                book_id = BOOK_IDS[genre]
                break

        if not book_id:
            pytest.skip("❌ book_id를 유추할 수 있는 마커가 없습니다.")

        if not is_book_home(driver):
            print(f"현재 위치가 작품홈이 아니므로 '{book_id}' 작품홈으로 이동합니다.")
            open_book_home(book_id)


def pytest_exception_interact(node, call, report):
    driver = node.funcargs.get("driver", None)
    if driver:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/fail_{node.name}_{timestamp}.png"
        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot(filename)
        print(f"\n❌ 실패 시 스크린샷 저장됨: {filename}")