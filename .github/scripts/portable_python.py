"""For tests only. Creates `cloud_py_api` in current directory and install portable python in it."""

from os import makedirs, path, remove
from platform import machine
from subprocess import DEVNULL, CalledProcessError, TimeoutExpired, run


def download_file(url: str, out_path: str) -> bool:
    n_download_clients = 2
    for _ in range(2):
        try:
            run(
                ["wget", "-q", "--no-check-certificate", url, "-O", out_path],
                timeout=90,
                stderr=DEVNULL,
                stdout=DEVNULL,
                check=True,
            )
            return True
        except (CalledProcessError, TimeoutExpired):
            break
        except FileNotFoundError:
            n_download_clients -= 1
            break
    for _ in range(2):
        try:
            run(["curl", "-L", url, "-o", out_path], timeout=90, stderr=DEVNULL, stdout=DEVNULL, check=True)
            return True
        except (CalledProcessError, TimeoutExpired):
            break
        except FileNotFoundError:
            n_download_clients -= 1
            break
    if not n_download_clients:
        raise EnvironmentError("Both curl and wget cannot be found.")
    return False


def python_install_to(out_path: str):
    py_url_start = "https://github.com/indygreg/python-build-standalone/releases/download/"
    py_url_ver_x64 = "20220502/cpython-3.9.12+20220502-aarch64-unknown-linux-gnu-install_only.tar.gz"
    py_url_ver_arm = "20220502/cpython-3.9.12+20220502-x86_64-unknown-linux-gnu-install_only.tar.gz"
    if machine().find("x64") != -1:
        py_url = py_url_start + py_url_ver_x64
    else:
        py_url = py_url_start + py_url_ver_arm
    makedirs(out_path, exist_ok=True)
    _archive_path = path.join(out_path, "download.tar.gz")
    download_file(py_url, _archive_path)
    _tar_cmd = f"tar -xf {_archive_path} -C {out_path} --strip-components 1"
    run(_tar_cmd.split(), check=True)
    remove(_archive_path)


if __name__ == "__main__":
    python_install_to("./cloud_py_api/python/")
