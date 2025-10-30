import pytest
from test_app.common.common_function import *
from test_app.common.common_elements import *
from test_app.platform.openApp import *
from test_app.platform.AppPlatform import *
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException


# 앱 최초실행 시 알림허용팝업
def test_permission_alert(driver, timeout=5):
    # native context로 전환
    driver.switch_to.context('NATIVE_APP')
    
    try:
        allow_button = permission_alert_popup(driver, timeout=timeout)
        if allow_button:
            allow_button.click()
            print("🔔 알림 허용 팝업 : 허용 완료")
        else:
            print("🔕 알림 팝업 미노출")

    except Exception as e:
        print(f"❗ 알림 팝업 처리 중 오류: {e}")

# 로그인
def test_login_app(driver):
    deeplink_login(driver, '4qatest', 'qwer1234!')


# 기기대체 팝업
def test_device_replacement_popup(driver, timeout=5):
    try:
        driver.switch_to.context('NATIVE_APP') 

        btn_radio = replace_firstdevice(driver)
        if btn_radio:
            btn_radio.click()
            assert btn_radio is not None, "❌ 첫번째 기기대체 실패"

            #'대체하기' 버튼 선택
            btn_replace = replace_device_complete(driver)
            btn_replace.click()
            assert btn_replace is not None, "❌ 기기대체 실패"

    except Exception as e:
        assert False, f"⚠️ '기기 대체' 팝업 처리 중 실패: {e}"

# 로그아웃
##
