import subprocess
import json

TAILSCALE_CMD = r"C:\Program Files\Tailscale\tailscale.exe"

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
