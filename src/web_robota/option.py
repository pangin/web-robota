import os

from selenium.webdriver.chrome import options
from .log_config import setup_logger


class _OptionBuilder:
    def __init__(self):
        self.__logger = setup_logger(__name__)
        self.__options = options.Options()
        self.__prefs = {}

        self.__logger.info('option builder initiated')

    def set_download_path(self, download_path: str):
        if not os.path.exists(download_path):
            self.__logger.info(f'creating download_path on {download_path}')
            os.makedirs(download_path)

        self.__prefs['download.default_directory'] = download_path

        self.__set_download_directory_set(True)
        self.__logger.info(f'download path set to {download_path}')

    def set_prompt_for_download(self, active_download_prompt: bool):
        self.__prefs['download.prompt_for_download'] = active_download_prompt
        self.__logger.info(f'download prompt set to {active_download_prompt}')

    def __set_download_directory_set(self, is_download_directory_set: bool):
        self.__prefs['download.directory_upgrade'] = is_download_directory_set
        self.__logger.info(f'download directory upgrade set to {is_download_directory_set}')

    def set_automatic_downloads(self, active_automatic_downloads: bool):
        if active_automatic_downloads:
            self.__prefs['profile.default_content_setting_values.automatic_downloads'] = 1
        elif not active_automatic_downloads:
            self.__prefs['profile.default_content_setting_values.automatic_downloads'] = 0
        else:
            raise ValueError(f'automatic downloads set failed')

        self.__logger.info(
            f'automatic downloads set to {self.__prefs['profile.default_content_setting_values.automatic_downloads']}')

    def set_headless(self):
        self.__options.add_argument('--headless=new')
        self.__logger.info('set headless mode')

    def set_no_sandbox(self):
        self.__options.add_argument('--no-sandbox')
        self.__logger.info('set no sandbox mode')

    def set_disable_gpu(self):
        self.__options.add_argument('--disable-gpu')
        self.__logger.info('set disable gpu')

    def set_disable_notifications(self):
        self.__options.add_argument('--disable-notifications')
        self.__logger.info('set disable notifications')

    def build(self):
        self.__logger.info('building options')
        self.__options.add_experimental_option('prefs', self.__prefs)

        return self.__options
