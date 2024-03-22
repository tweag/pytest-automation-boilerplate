import os
import platform
import shutil
import requests

from main.utils.env_variables import EnvVariables

BROWSERSTACK_LOCAL_MAC = (
    "https://www.browserstack.com/browserstack-local/BrowserStackLocal-darwin-x64.zip"
)
BROWSERSTACK_LOCAL_LINUX = (
    "https://www.browserstack.com/browserstack-local/BrowserStackLocal-linux-x64.zip"
)
BROWSERSTACK_LOCAL_WINDOWS = (
    "https://www.browserstack.com/browserstack-local/BrowserStackLocal-win32.zip"
)

BINARY_NAMES = ["chromedriver", "geckodriver", "msedgedriver", "BrowserStackLocal"]
DO_NOT_DELETE_DURING_CLEANUP = [".gitkeep"]

env_variable = EnvVariables()


def _clean_binaries_dir(dir):
    for item in os.listdir(dir):
        item = item.split('.')[0] if '.exe' in item and item.split('.')[0] in BINARY_NAMES else item
        if item not in BINARY_NAMES and item not in DO_NOT_DELETE_DURING_CLEANUP:
            item_path = f"{dir}/{item}"
            shutil.rmtree(item_path) if os.path.isdir(item_path) else os.remove(item_path)


def _unzip(zip_file, unzip_dir):
    stream = os.popen("unzip -o %s -d %s" % (zip_file, unzip_dir))
    output = stream.read()
    _clean_binaries_dir(unzip_dir)
    print(output)


def _create_dir_if_needed(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def _download_file(url, dest_path):
    response = requests.get(url, allow_redirects=True)
    with open(dest_path, "wb") as f:
        f.write(response.content)


def _download_platform_specific_file(
    name, temp_dir, dest_dir, platform_url_map, platform_filename_map
):
    platform_type = platform.system().lower()
    print(f"Downloading {name} for {platform_type} platform")

    _create_dir_if_needed(temp_dir)

    download_filename = platform_filename_map[platform_type]
    download_path = temp_dir + f"/{download_filename}"
    _download_file(platform_url_map[platform_type], download_path)

    _create_dir_if_needed(dest_dir)
    _unzip(download_path, dest_dir)
    print(f"'{name}' saved at location: {dest_dir} \n")


def get_bs_local_by_platform(temp_dir, scripts_dir):
    platform_url_map = {
        "darwin": BROWSERSTACK_LOCAL_MAC,
        "linux": BROWSERSTACK_LOCAL_LINUX,
        "windows": BROWSERSTACK_LOCAL_WINDOWS,
    }

    bs_filename = "BrowserstackLocal.zip"
    platform_filename_map = {
        "darwin": bs_filename,
        "linux": bs_filename,
        "windows": bs_filename,
    }

    _download_platform_specific_file(
        "Browserstack Local - Latest",
        temp_dir,
        scripts_dir,
        platform_url_map,
        platform_filename_map,
    )
