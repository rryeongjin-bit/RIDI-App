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
    return find_element_auto(driver, AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().description("총 15화")')

# 최신순 정렬버튼
def sort_episode_recently(driver:WebDriver):
    return find_element_auto(driver, AppiumBy.ANDROID_UIAUTOMATOR,
                             'new UiSelector().text("최신순")')

# 웹툰_15회차 다운로드 버튼
def webtoon_episode_15(driver:WebDriver):
    return find_element_auto(driver, AppiumBy.ANDROID_UIAUTOMATOR,
                             'new UiSelector().className("android.widget.ImageView").instance(3)')

# # 회차리스트 프레임
# def get_episode_list(driver: WebDriver):
#     return driver.find_elements(
#         AppiumBy.ANDROID_UIAUTOMATOR,
#         'new UiSelector().resourceId("themedView")'
#     )
# def get_ownership_label(driver:WebDriver):
#     return find_element_auto(driver,AppiumBy.ID, 'ownershipLabel')


# def get_download_button(driver:WebDriver, index_from_last=0):
#     """
#     회차(episode_element) 안의 ImageView들 중 최상단(n번째) 요소를 다운로드 버튼으로 가정하고 반환.
#     기본적으로 최상단 첫번째 요소를 클릭함 (index_from_last=0).
#     """
#     image_views = find_element_auto(driver,AppiumBy.CLASS_NAME, 'android.widget.ImageView')

#     if not image_views:
#         raise NoSuchElementException("❌ ImageView 요소가 없습니다.")

#     try:
#         return image_views[index_from_last]
#     except IndexError:
#         raise NoSuchElementException(f"❌ ImageView[{index_from_last}] 요소를 찾을 수 없습니다.")

def modal_popup_payment_rent(driver:WebDriver):
    return find_element_auto(driver, AppiumBy.XPATH, '//main/div/div/section/div[2]/div/div/div/div[1]/button[1]')

def payment_rent(driver:WebDriver):
    return find_element_auto(driver, AppiumBy.XPATH, '//main/div/div/section/div[2]/div/div/div/div[2]/div/div[2]/button')
