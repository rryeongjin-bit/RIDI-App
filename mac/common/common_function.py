import time
import subprocess
from test_app.platform.openApp import open_app, AppType
from test_app.common.common_elements import *
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

# 딥링크 - 작품홈
def open_book_home(book_id):
    deep_link = f'ridi://ContentsHome/"{book_id}"'
    adb_command = f'adb shell am start -a android.intent.action.VIEW -d "{deep_link}"'
    subprocess.run(adb_command, shell=True)

    time.sleep(2)

# 딥링크 - My
def deeplink_my():
    deep_link = f'ridi://MyRidi'
    adb_command = f'adb shell am start -a android.intent.action.VIEW -d "{deep_link}"'
    subprocess.run(adb_command, shell=True)

    time.sleep(2)

# 컨텍스트 전환 함수 (현재 컨텍스트가 NATIVE_APP이면 WebView로, WebView면 NATIVE_APP으로 전환)
def toggle_context(driver, target=None):
    """
    컨텍스트 전환 함수 (현재 컨텍스트가 NATIVE_APP이면 WebView로, WebView면 NATIVE_APP으로 전환)
    """
    try:
        current = driver.current_context
        contexts = driver.contexts
        print(f"🔍현재 컨텍스트: {current}")
        print(f"📱사용 가능한 컨텍스트 목록: {contexts}")

        if target:
            if target in contexts:
                driver.switch_to.context(target)
                print(f"✅명시적 컨텍스트 전환: {target}")
            else:
                raise Exception(f"❌목표 컨텍스트 '{target}'를 찾을 수 없음")
        else:
            if current == "NATIVE_APP":
                for context in contexts:
                    if 'WEBVIEW' in context:
                        driver.switch_to.context(context)
                        print(f"✅WebView로 전환: {context}")
                        return
                raise Exception("❌WebView 컨텍스트를 찾을 수 없습니다.")
            else:
                driver.switch_to.context("NATIVE_APP")
                print("✅네이티브 앱으로 전환 완료")
    except Exception as e:
        raise Exception(f"❌컨텍스트 전환 실패: {e}")

def is_logged_in(driver):
    """
    현재 로그인/로그아웃 상태를 판단하는 헬퍼 함수
    """
    try:
        deeplink_my()
        logout_element = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("로그아웃")')
        if logout_element:
            return True
    except:
        return False


# 딥링크 - 로그인 (전제조건 : 로그아웃 상태여야 실행됨)
def deeplink_login(driver, id, pw):
    deep_link = f'ridi://SignIn'
    adb_command = f'adb shell am start -a android.intent.action.VIEW -d "{deep_link}"'
    subprocess.run(adb_command, shell=True)
    time.sleep(3)

    try:	
        # ID 입력 필드 찾고 입력
        id_field = driver.find_element(AppiumBy.ID, 'com.initialcoms.ridi.staging:id/login_id')
        id_field.click()
        id_field.send_keys(id)

        # PW 입력 필드 찾고 입력
        pw_field = driver.find_element(AppiumBy.ID,'com.initialcoms.ridi.staging:id/login_password')
        pw_field.click()
        pw_field.send_keys(pw)

        # 로그인 버튼 클릭
        login_button = driver.find_element(AppiumBy.ID, 'com.initialcoms.ridi.staging:id/login_button')
        login_button.click()

        print("✅ 로그인 성공")



    except Exception as e:
        print(f"❌ 로그인 실패: {e}")


def is_book_home(driver, timeout = 1):
    """
    현재 위치가 작품홈인지 판단하는 헬퍼 함수
    """
    
    selectors = [
        ('ANDROID_UIAUTOMATOR', 'new UiSelector().resourceId("QA-작품홈-네비바-작품명")'),
        ('ANDROID_UIAUTOMATOR', 'new UiSelector().resourceId("QA-작품홈-헤더-작품명")'),
        ('ANDROID_UIAUTOMATOR', 'new UiSelector().resourceId("QA-전체회차목록-네비바-타이틀")'),
        ('ANDROID_UIAUTOMATOR', 'new UiSelector().resourceId("QA-선택구매-네비바-타이틀")')
    ]

    for by, value in selectors:
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((getattr(AppiumBy, by),value))
            )
            return True
        except:
            continue
    return False


# 좌우스와이프 함수
def swipe_left_right(driver, start_x=0.9, end_x=0.1, y=0.5, duration=800):

    screen_size = driver.get_window_size()
    width = screen_size['width']
    height = screen_size['height']

    start_x = int(width * start_x)
    end_x = int(width * end_x)
    y = int(height * y)

    pointer = PointerInput("touch", "touch")
    actions = ActionBuilder(driver)

    actions.pointer_action.move_to_location(start_x, y) 
    actions.pointer_action.pointer_down()  
    actions.pointer_action.pause(duration / 1000)  
    actions.pointer_action.move_to_location(end_x, y) 
    actions.pointer_action.pointer_up() 

    actions.perform()
    time.sleep(3) 

# 상하스크롤 함수
def swipe_up_down(driver, start_x=0.5, start_y=0.8, end_y=0.2, duration=800):

    screen_size = driver.get_window_size()
    width = screen_size['width']
    height = screen_size['height']

    start_x = int(width * start_x)
    start_y = int(height * start_y)
    end_y = int(height * end_y)

    pointer = PointerInput("touch", "touch")
    actions = ActionBuilder(driver)

    actions.pointer_action.move_to_location(start_x, start_y) 
    actions.pointer_action.pointer_down() 
    actions.pointer_action.pause(duration / 1000) 
    actions.pointer_action.move_to_location(start_x, end_y)  
    actions.pointer_action.pointer_up() 

    actions.perform()
    time.sleep(3) 


