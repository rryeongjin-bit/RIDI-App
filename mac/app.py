import json
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)
TAILSCALE_CMD = "/Applications/Tailscale.app/Contents/MacOS/Tailscale"

def get_tailscale_status():
    try:
        result = subprocess.run([TAILSCALE_CMD, "status", "--json"], capture_output=True, text=True)
        if result.returncode != 0:
            return "⚠️ Tailscale 정보 조회 실패"

        status = json.loads(result.stdout)
        self_node = status.get("Self", {})
        exit_node_status = status.get("ExitNodeStatus")
        peers = status.get("Peer", {})

        is_online = self_node.get("Online", False)

        # OFF이거나 ExitNode가 없는 경우
        if not is_online or not exit_node_status or not exit_node_status.get("ID"):
            return "env-prod"

        # Exit Node 이름 찾기
        exit_node_id = exit_node_status["ID"]
        exit_node_name = next(
            (peer.get("HostName") or peer.get("DNSName") for peer in peers.values() if peer.get("ID") == exit_node_id),
            exit_node_id  # fallback
        )

        # Exit Node 이름 기반 이모지 판별
        if "canary" in exit_node_name:
            return "env-canary"
        elif "stage" in exit_node_name:
            return "env-stage"
        elif "dev" in exit_node_name:
            return "env-dev"
        else:
            return f"{exit_node_name}"

    except Exception as e:
        return f"⚠️ Tailscale 상태 확인 중 오류: {str(e)}"


# 1. 슬래시 커맨드 요청 받아서 모달 띄우기
@app.route('/run_test', methods=['POST'])
def run_test_command():
    trigger_id = request.form.get('trigger_id')

    # 슬랙 모달 띄우기 JSON 구조 (예시)
    modal_view = {
        "type": "modal",
        "callback_id": "test_modal",
        "title": {"type": "plain_text", "text": "테스트 실행"},
        "submit": {"type": "plain_text", "text": "실행"},
        "blocks": [
            # 여기 모달 입력 폼 작성
        ]
    }

    # 슬랙 API 호출로 모달 띄우기 (requests.post 필요)
    # 또는 슬랙 Bolt 라이브러리 사용 가능
    # 여기선 간략히 생략

    return "", 200  # 슬랙 Slash Command는 200 OK 즉시 응답 필요

# 2. 모달 제출 시 인터랙티브 요청 처리
@app.route('/slack/interactive', methods=['POST'])
def slack_interactive():
    data = request.json
    # 모달 제출 데이터 파싱
    platform = data['actions'][0]['selected_option']['value']
    device = data['actions'][1]['value']
    username = data['actions'][2]['value']
    password = data['actions'][3]['value']

    # 자동화 스크립트 실행
    subprocess.run(["python", "appium_test.py", platform, device, username, password])

    return jsonify({"response_action": "clear"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)




    # flask서버 포트 기본 5000으로 설정 원복
    # ngrok http 7000 > forwarding url 지정했으나 오류발생 
    # ngrok > pkill ngrok 실행상태    
    # 나중에 다시 셋팅해야할것 > slack api 에서 slash command 지정다시하기