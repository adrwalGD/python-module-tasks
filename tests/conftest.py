import subprocess
import time
import pytest
import requests


def wait_for_server(url: str, timeout: int = 5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            res = requests.get(url)
            if res.status_code == 200:
                return
        except requests.exceptions.ConnectionError:
            time.sleep(0.05)

    raise TimeoutError(f"Server did not start in {timeout} seconds")


@pytest.fixture
def run_api_server():
    """Run API server, for single test function. Needed to reset state."""
    proc = subprocess.Popen(["python3", "-m", "python_module_tasks.advanced.api.main"])

    wait_for_server("http://localhost:8000")
    yield

    proc.terminate()
    proc.wait()
