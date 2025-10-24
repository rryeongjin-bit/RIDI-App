import pytest
from test_app.common.common_function import *
from test_app.common.common_elements import *
from test_app.test_platform.openApp import *
from test_app.test_platform.AppPlatform import *
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

# 작품홈 > 전체회차 진입
@pytest.mark.bookhome
@pytest.mark.webtoon
def test_webtoon_bookhome(driver:WebDriver):
    # anchor_episode_tab = episode_tab(driver)
    # anchor_episode_tab.click()
    # assert anchor_episode_tab is not None, "❌ Failed : 회차탭 선택 실패"

    #전체 회차리스트 진입
    episode_total = episode_list_total(driver)
    if episode_total:
        episode_total.click()
    assert episode_total is not None, "❌ Failed : 전체회차 진입 실패"

@pytest.mark.bookhome
@pytest.mark.preconditioned
def test_click_first_available_episode(driver:WebDriver):
    sort_recently = sort_episode_recently(driver)
    sort_recently.click()
    assert sort_recently is not None, "❌ Failed : 최신순 정렬 실패"

    try:
        btn_episode = webtoon_episode_recent(driver)
        if btn_episode:
            btn_episode.click()

            # WebView 컨텍스트 전환 시도
            toggle_context(driver)
            current_context = driver.current_context
            if "WEBVIEW" not in current_context:
                raise Exception("❌ WebView 전환 실패")

            # WebView 내 결제 모달 요소 확인
            try:
                modal_tab = modal_popup_payment_rent(driver)
                assert modal_tab is not None, "❌ 결제 모달 요소가 존재하지 않음"
                print("✅ WebView에서 결제 모달 정상 노출")
                return 
            except (NoSuchElementException, AssertionError) as e:
                raise Exception(f"❌ WebView 전환 후 결제 모달 요소 확인 실패: {e}")

    except Exception as e:
        raise AssertionError(f"❌ 회차 다운로드 버튼 선택 실패: {e}")


@pytest.mark.bookhome
@pytest.mark.preconditioned
def test_payment_rent_webtoon(driver:WebDriver):

   # WebView로 컨텍스트 전환
    toggle_context(driver)
    current_context_after_webview = driver.current_context
    webview_success = "WEBVIEW" in current_context_after_webview

    modal_tab = modal_popup_payment_rent(driver)
    modal_tab.click()

    modal_rent_button = payment_rent(driver)
    modal_rent_button.click()

    # 네이티브 앱으로 컨텍스트 복귀
    toggle_context(driver)
    current_context_after_native = driver.current_context
    native_success = current_context_after_native == "NATIVE_APP"
    
    # ✅ 단일 assert로 실패 메시지 통합 출력
    assert (
        webview_success and
        native_success
    ), (
        "❌ 결제테스트 실패"
        f" - WebView 컨텍스트 진입 여부: {'성공' if webview_success else '실패'}\n"
        f" - 결제 후 네이티브 전환 여부: {'성공' if native_success else '실패'}\n"
        f"👉 현재 컨텍스트: {driver.current_context}"
    )

    btn_paymnet_episode = payment_rent(driver)
    if btn_paymnet_episode:
        btn_paymnet_episode.click()
        assert btn_paymnet_episode is not None, "❌ 대여로 결제하기 실패"


@pytest.mark.bookhome
@pytest.mark.preconditioned
# 카트진입
def test_cart(driver:WebDriver):
    deeplink_my(driver)

    enter_cart = cart(driver)
    enter_cart.click()
    # WebView로 컨텍스트 전환
    toggle_context(driver)

    enter_cart_page = cart_page(driver)
    assert enter_cart_page is not None, "❌ 카트 진입 실패"

        
@pytest.mark.bookhome
@pytest.mark.preconditioned
@pytest.mark.delete_after_test
# 로그아웃
def test_logout_app(driver:WebDriver):
    deeplink_my(driver)

    btn_logout = logout(driver)
    btn_logout.click

    try:
        popup_logout = logout_check(driver)

    except:
        assert False, "❌ 로그아웃 버튼 선택 실패"