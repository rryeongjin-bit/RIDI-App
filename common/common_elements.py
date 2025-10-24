from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# ───────────────────────────────────────────────────────────────
# 📌 테스트 도서
# ───────────────────────────────────────────────────────────────
BOOK_IDS = {
    "webtoon": "4116004613",       # 살인마는 갈색머리 영애를 노린다
    "webnovel": "6006000001",      # 방백
}

# ───────────────────────────────────────────────────────────────
# 📌 요소선언 함수
# ───────────────────────────────────────────────────────────────

def find_element_auto(driver, by, value, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        elements = driver.find_elements(by, value)
        return elements[0] if elements else None
    except:
        return None
    
# ───────────────────────────────────────────────────────────────
# 📌 공통
# ───────────────────────────────────────────────────────────────

# 앱알림 허용 팝업 >  허용버튼
def permission_alert_popup(driver, timeout=5):
     return find_element_auto(driver,AppiumBy.ID,'com.android.permissioncontroller:id/permission_allow_button')

# 기기대체 팝업 > 기기대체 타이틀
def replace_device(driver:WebDriver):
    return find_element_auto(driver,AppiumBy.ID, 'om.initialcoms.ridi.staging:id/title')

# 기기대체 팝업의 첫번째 라디오버튼
def replace_firstdevice(driver:WebDriver):
    return find_element_auto(driver,AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.initialcoms.ridi.staging:id/selection_radio_button").instance(0)')

# 기기대체하기
def replace_device_complete(driver:WebDriver):
    return find_element_auto(driver,AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.initialcoms.ridi.staging:id/replace_button").textContains("대체하기")')

# ───────────────────────────────────────────────────────────────
# 📌 작품홈
# ───────────────────────────────────────────────────────────────

# 회차 앵커탭
def episode_tab(driver:WebDriver):
    return find_element_auto(driver,AppiumBy.ANDROID_UIAUTOMATOR,
                             'new UiSelector().description("회차").instance(1)')

# 전체회차리스트 진입
def episode_list_total(driver:WebDriver):
    return find_element_auto(driver, AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("QA-작품홈-회차목록-더보기")')

# 최신순 정렬버튼
def sort_episode_recently(driver:WebDriver):
    return find_element_auto(driver, AppiumBy.ANDROID_UIAUTOMATOR,
                             'new UiSelector().text("최신순")')

# 웹툰_최신회차_다운로드 버튼
def webtoon_episode_recent(driver:WebDriver):
    return find_element_auto(driver, AppiumBy.XPATH, '//android.view.ViewGroup[@resource-id="QA-전체회차목록-0-다운로드"]/android.widget.ImageView')


def modal_popup_payment_rent(driver:WebDriver):
    return find_element_auto(driver, AppiumBy.XPATH, '//main/div/div/section/div[2]/div/div/div/div[1]/button[1]')

def payment_rent(driver:WebDriver):
    return find_element_auto(driver, AppiumBy.XPATH, '//main/div/div/section/div[2]/div/div/div/div[2]/div/div[2]/button')


# ───────────────────────────────────────────────────────────────
# 📌 MY리디
# ───────────────────────────────────────────────────────────────

# 카트
def cart(driver:WebDriver):
    return find_element_auto(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("카트, 113개")') 


# 카트진입
def cart_page(driver:WebDriver):
    return find_element_auto(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("카트").instance(0)')


# 로그아웃
def logout(driver:WebDriver):
    return find_element_auto(driver, AppiumBy.ID, '로그아웃')

# 로그아웃 확인 팝업
def logout_check(driver:WebDriver):
    return find_element_auto(driver, AppiumBy.ID, 'com.initialcoms.ridi.staging:id/dialog_title')

# 로그아웃 버튼
def logout_check_btn(driver:WebDriver):
    return find_element_auto(driver,AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("로그아웃")')
