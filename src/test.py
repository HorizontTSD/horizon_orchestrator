import subprocess

containers = [
    {
        "name": "horizon_orchestrator_auth",
        "env": "horizon/horizon_orchestrator/.env",
        "host_port": 8603,
        "container_port": 7070,
        "image": "d97fd3fc269b"
    },
    {
        "name": "set_schedule_forecast_horizon",
        "env": "horizon/set_schedule_forecast_horizon/.env",
        "host_port": 8084,
        "container_port": 7070,
        "image": "bc96a6129012"
    },
    {
        "name": "set_schedule_forecast_tool",
        "env": "Study/tool_backend/.env",
        "host_port": 7070,
        "container_port": 7070,
        "image": "c2177ee3f4c7"
    },
    {
        "name": "schedule_prediction",
        "env": "horizon/schedule_prediction/.env",
        "host_port": 7072,
        "container_port": 7070,
        "image": "8d963194a890"
    },
    {
        "name": "auth_service_horizon",
        "env": "horizon/auth_service_horizon/.env",
        "host_port": 8601,
        "container_port": 7070,
        "image": "7e0ebabcc437"
    },
]


id_services = [
    {
        "name": "ats_synthtic_data",
        "image_id": "963353af4044"
    }
]

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def kill_docker_process_on_port(port):
    container_id, _, _ = run_cmd(f"sudo docker ps --filter publish={port} --format '{{{{.ID}}}}'")
    if container_id:
        pid, _, _ = run_cmd(f"sudo docker inspect -f '{{{{.State.Pid}}}}' {container_id}")
        if pid:
            print(f"Убиваю процесс {pid} контейнера {container_id}, занявший порт {port}")
            run_cmd(f"sudo kill -9 {pid}")

def start_container(c):
    try:
        kill_docker_process_on_port(c["host_port"])
        stdout, stderr, code = run_cmd(
            f"sudo docker run -d --restart always --env-file {c['env']} "
            f"-p {c['host_port']}:{c['container_port']} {c['image']}"
        )
        if code == 0 and stdout:
            print(f"[OK] {c['name']} запущен, container_id: {stdout}")
        else:
            print(f"[ERR] {c['name']} не запущен\nSTDOUT: {stdout}\nSTDERR: {stderr}")
    except Exception as e:
        print(f"[EXC] Ошибка при запуске {c['name']}: {e}")



def start_id_service(s):
    try:
        stdout, stderr, code = run_cmd(
            f"sudo docker run -d --restart always {s['image_id']}"
        )
        if code == 0 and stdout:
            print(f"[OK] {s['name']} запущен, container_id: {stdout}")
        else:
            print(f"[ERR] {s['name']} не запущен\nSTDOUT: {stdout}\nSTDERR: {stderr}")
    except Exception as e:
        print(f"[EXC] Ошибка при запуске {s['name']}: {e}")

if __name__ == "__main__":
    for c in containers:
        print(f"Запуск контейнера {c['name']} на порту {c['host_port']}...")
        start_container(c)

    for s in id_services:
        print(f"Запуск контейнера по image_id {s['image_id']}...")
        start_id_service(s)


