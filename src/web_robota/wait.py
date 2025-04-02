import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from .log_config import setup_logger
from .const import FILE_EXTENSION_CRDOWNLOAD, FILE_EXTENSION_TMP
from .timeout import timeout
from .type import SimpleInstruction


class _Wait:
    def __init__(self, driver: webdriver):
        self.__logger = setup_logger(__name__)
        self.__driver = driver
        self.__logger.info('wait module initiated')

    def until_time(self, seconds: float):
        self.__logger.info(f'waiting for {seconds} seconds')
        time.sleep(seconds)

    def until_download_finished(self, download_path: str, expected_file_num: int, timeout_seconds: int = SimpleInstruction.timeout):
        @timeout(timeout_seconds)
        def do():
            self.__logger.info(f'waiting {timeout_seconds} seconds for {expected_file_num} files download to complete in {download_path}')
            is_download_completed = False

            while is_download_completed is False:
                files = os.listdir(download_path)
                is_download_completed = True

                if expected_file_num <= len(files):
                    for file_name in files:
                        if file_name.endswith(FILE_EXTENSION_CRDOWNLOAD):
                            is_download_completed = False
                        elif file_name.endswith(FILE_EXTENSION_TMP):
                            is_download_completed = False
                else:
                    is_download_completed = False

            self.__logger.info('download completed')

        do()

    def for_element(self, instruction: SimpleInstruction):
        self.__logger.info(f'waiting {instruction.timeout} seconds for element {instruction.element['name']} to appear')

        if instruction.timeout == 0:
            return

        wait = WebDriverWait(self.__driver, instruction.timeout)

        wait.until(expected_conditions.visibility_of_element_located((By.XPATH, instruction.element['xpath'])))

    def for_one_of_element(self, instructions: list[SimpleInstruction]):
        self.__logger.info(f'waiting for element to appear in one of {len(instructions)} elements')

        valid_instruction = None

        for instruction in instructions:
            try:
                self.__logger.info(f'trying to wait for {instruction.element['name']} to appear')
                self.for_element(instruction)

                valid_instruction = instruction

                break
            except Exception:
                self.__logger.error(f'failed to wait for {instruction.element['name']} to appear')

        if valid_instruction is None:
            self.__logger.error('failed to wait for any elements to appear')

            raise ValueError('failed to wait for any elements to appear')

        return valid_instruction

    def for_elements(self, instructions: list[SimpleInstruction]):
        self.__logger.info(f'waiting for {len(instructions)} elements to appear')

        for instruction in instructions:
            self.for_element(instruction)

    def for_site_load_complete(self, timeout_seconds: int = SimpleInstruction.timeout):
        @timeout(timeout_seconds)
        def do():
            self.__logger.info(f'waiting for site to load in {timeout_seconds} seconds')

            while True:
                ready_state = self.__driver.execute_script('return document.readyState')

                if ready_state == 'complete':
                    self.__logger.info('site loaded')

                    break

    def for_target_site_load_complete(self, url: str, timeout_seconds: int = SimpleInstruction.timeout):
        @timeout(timeout_seconds)
        def do():
            self.__logger.info(f'waiting for site {url} to load in {timeout_seconds} seconds')

            while True:
                if url in self.__driver.current_url:
                    self.__logger.info(f'site {url} loaded')

                    break