import os
import json
import subprocess
from appium import webdriver
from test_app.platform.AppPlatform import PlatformType
from appium.options.android import UiAutomator2Options
from enum import Enum

# 앱 유형을 Enum으로 정의
class AppType(Enum):
    PROD = 'com.initialcoms.ridi'
    STAGING = 'com.initialcoms.ridi.staging'
    PROD_ONESTORE = 'com.ridi.books.onestore'
    STAGING_ONESTORE = 'com.ridi.books.onestore.staging'

# ios의 경우 현재 실행된 시뮬레이터의 udid값을 알아서 찾아서 가져오도록 함
def get_booted_ios_simulator_udid():
    try:
        output = subprocess.check_output(["xcrun", "simctl", "list", "devices", "booted", "-j"])
        data = json.loads(output)
        devices = data['devices']
        for runtime in devices:
            for device in devices[runtime]:
                if device.get('state') == 'Booted':
                    return device['udid']
    except Exception as e:
        print(f"Error getting iOS simulator UDID: {e}")
        raise

def open_app(app_type: Enum, platform: str, device_name: str, port: int):
    appium_server_url = f"http://localhost:{port}"  

    if platform == PlatformType.ANDROID:
        apk_path = "/Users/ridi/Desktop/appfile/RIDI-25.113.3-Playstore.apk"
        
        app_activities = {
            AppType.PROD: 'com.ridi.books.viewer.main.activity.SplashActivity',
            AppType.STAGING: 'com.ridi.books.viewer.main.activity.SplashActivity',
            AppType.PROD_ONESTORE: 'com.ridi.books.viewer.main.activity.SplashActivity',
            AppType.STAGING_ONESTORE: 'com.ridi.books.viewer.main.activity.SplashActivity',
        }
        app_package = app_type.value
        app_activity = app_activities[app_type]
        
        # # 앱 수동 실행
        # os.system(f"adb shell am start -n {app_package}/{app_activity}")

        options = UiAutomator2Options()
        options.platform_name = "android"
        options.automation_name = "uiautomator2"
        options.device_name = device_name
        options.app_package = app_package
        options.app_activity = app_activity
        options.app = apk_path
        options.no_reset = True
        options.set_capability("ignoreUnimportantViews", True)

        driver = webdriver.Remote(appium_server_url, options=options)
        return driver, app_package 

    elif platform == PlatformType.IOS:
        #Import Error 방지
        from appium.options.ios import XCUITestOptions 

        ipa_path =  "/Users/ridi/Desktop/appfile/Ridibooks for Appium.app"  

        options = XCUITestOptions()
        options.platform_name = "ios"
        options.automation_name = "XCUITest"
        options.device_name = device_name
        options.platform_version = "17.5"
        options.app = ipa_path  
        options.no_reset = True  
        options.xcode_org_id = "SNTDSH9YYM"
        options.xcode_signing_id = "iPhone Developer"
        options.set_capability("ignoreUnimportantViews", True)

        driver = webdriver.Remote(appium_server_url, options=options)

    else:
        raise ValueError(f"Unsupported platform: {platform}")

    return driver

