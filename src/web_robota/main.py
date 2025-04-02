import os
from collections import namedtuple

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

from .log_config import setup_logger
from .option import _OptionBuilder
from .timeout import timeout
from .type import SimpleInstruction
from .wait import _Wait


class WebRobota:
    def __init__(self, name: str | None = 'no_name'):
        self.__logger = setup_logger(__name__)
        self.name = name
        self.wait: _Wait | None = None
        self.__driver: selenium.webdriver.Chrome | None = None
        self.option_builder = _OptionBuilder()

    def __del__(self):
        self.quit()

    def boot_up(self):
        self.__logger.info('boot up web_robota')

        option = self.option_builder.build()
        self.__driver = webdriver.Chrome(options=option)
        self.wait = _Wait(driver=self.__driver)

    # TODO: Action Chain 구현
    # def create_action_chain(self):
    #     self.__logger.error('action chain is not supported')

    def set_window_size(self, width, height):
        self.__logger.info(f'setting window size to {width}, {height}')
        self.__driver.set_window_size(width, height)

    def set_window_position(self, x: float, y: float):
        self.__logger.info(f'setting window position to {x}, {y}')
        self.__driver.set_window_position(x=x, y=y)

    def change_download_path(self, download_path: str):
        self.__logger.info(f'changing download path to {download_path}')

        if not os.path.exists(download_path):
            self.__logger.info(f'creating download path on {download_path}')
            os.makedirs(download_path)

        change_download_path_params = {'behavior': 'allow', 'downloadPath': download_path}

        self.__driver.execute_cdp_cmd('Browser.setDownloadBehavior', change_download_path_params)
        self.__logger.info(f'download path changed to {download_path}')

    def get_current_url(self):
        current_url = self.__driver.current_url

        self.__logger.info(f'current url : {current_url}')

        return current_url

    def go_to(self, url: str, timeout_seconds: int = SimpleInstruction.timeout):
        if url == self.get_current_url():
            self.__logger.info(f'already at {url}')

            return

        self.__logger.info(f'traveling to {url}')
        self.__driver.get(url=url)
        self.wait.for_site_load_complete(timeout_seconds=timeout_seconds)

    def find_element(self, instruction: SimpleInstruction):
        @timeout(instruction.timeout)
        def do_find_element():
            self.wait.for_element(instruction)

            element = self.__driver.find_element(By.XPATH, instruction.element['xpath'])

            return element

        return do_find_element()

    def find_elements(self, instructions: list[SimpleInstruction] | SimpleInstruction):
        if type(instructions) != list:
            @timeout(instructions.timeout)
            def do_find_elements():
                self.wait.for_element(instructions)

                elements = self.__driver.find_elements(By.XPATH, instructions.element['xpath'])

                return elements

            return do_find_elements()

        elements = []

        for instruction in instructions:
            element = self.find_element(instruction)

            elements.append(element)

        return elements

    def click(self, instruction: SimpleInstruction):
        @timeout(instruction.timeout)
        def do_click():
            self.__logger.info(f'clicking on {instruction.element['name']}')
            self.wait.for_element(instruction)

            element_to_click = self.__driver.find_element(By.XPATH, instruction.element['xpath'])

            element_to_click.click()

        do_click()

    def click_one_of_elements(self, instructions: list[SimpleInstruction]):
        self.__logger.info(f'clicking on one of {len(instructions)} elements')

        valid_instruction = None

        self.wait.for_elements(instructions)

        for instruction in instructions:
            try:
                self.__logger.info(f'trying to click on {instruction.element['name']}')
                self.click(instruction)

                valid_instruction = instruction

                break
            except Exception:
                self.__logger.warning(f'failed to click on {instruction.element['name']}')

        if valid_instruction is None:
            self.__logger.error('failed to click on any elements')

            raise ValueError('failed to click on any elements')

        return valid_instruction

    def click_elements(self, instructions: list[SimpleInstruction]):
        self.__logger.info(f'clicking on {len(instructions)} elements')

        for instruction in instructions:
            try:
                self.click(instruction)
            except Exception:
                self.__logger.warning(f'failed to click on {instruction.element['name']}')

    def input(self, instruction: SimpleInstruction):
        self.__logger.info(f'inputting on {instruction.element['name']}')
        self.wait.for_element(instruction)

        element_to_input = self.__driver.find_element(By.XPATH, instruction.element['xpath'])

        element_to_input.send_keys(instruction.value)

    def input_one_of_elements(self, instructions: list[SimpleInstruction]):
        self.__logger.info(f'inputting on one of {len(instructions)} elements')

        valid_instruction = None

        for instruction in instructions:
            try:
                self.__logger.info(
                    f'trying to input on {instruction.element['name']} with value {instruction.value}')
                self.input(instruction)

                valid_instruction = instruction

                break
            except Exception:
                self.__logger.error(
                    f'failed to input on {instruction.element['name']} with value {instruction.value}')

        if valid_instruction is None:
            self.__logger.error('failed to input on any elements')

            raise ValueError('failed to input on any elements')

        return valid_instruction

    def input_on_elements(self, instructions: list[SimpleInstruction]):
        self.__logger.info(f'inputting on {len(instructions)} elements')

        for instruction in instructions:
            try:
                self.input(instruction)
            except Exception:
                self.__logger.error(f'failed to input on {instruction.element['name']}')

    def clear_input(self, instruction: SimpleInstruction):
        self.__logger.info(f'clearing input on {instruction.element['name']}')
        self.wait.for_element(instruction)

        element_to_clear = self.__driver.find_element(By.XPATH, instruction.element['xpath'])

        element_to_clear.clear()

    def clear_inputs(self, instructions: list[SimpleInstruction]):
        self.__logger.info(f'clearing inputs on {len(instructions)} elements')

        for instruction in instructions:
            try:
                self.clear_input(instruction)
            except Exception:
                self.__logger.error(f'failed to clear input on {instruction.element['name']}')

    def clear_one_of_inputs(self, instructions: list[SimpleInstruction]):
        self.__logger.info(f'clearing inputs on one of {len(instructions)} elements')

        valid_instruction = None

        for instruction in instructions:
            try:
                self.__logger.info(f'trying to clear input on {instruction.element['name']}')
                self.clear_input(instruction)

                valid_instruction = instruction

                break
            except Exception:
                self.__logger.warning(f'failed to clear input on {instruction.element['name']}')

        if valid_instruction is None:
            self.__logger.error('failed to clear input on any elements')

            raise ValueError('failed to clear input on any elements')

        return valid_instruction

    def get_string_from_element(self, instruction: SimpleInstruction):
        self.__logger.info(f'getting string from {instruction.element['name']}')
        self.wait.for_element(instruction)

        element_to_get_string = self.__driver.find_element(By.XPATH, instruction.element['xpath'])
        string_from_element = element_to_get_string.text

        self.__logger.info(f'string from {instruction.element['name']}: {string_from_element}')

        return string_from_element

    def get_strings_from_elements(self, instructions: list[SimpleInstruction] | SimpleInstruction):
        Result = namedtuple('Result', ['instruction', 'string'])

        if type(instructions) != list:
            @timeout(instructions.timeout)
            def do_get_strings_from_elements():
                self.wait.for_element(instructions)

                string_from_elements = []
                elements = self.__driver.find_elements(By.XPATH, instructions.element['xpath'])

                for element in elements:
                    result = Result(instruction=instructions, string=element.text)
                    string_from_elements.append(result)

                return string_from_elements

            return do_get_strings_from_elements()

        self.__logger.info(f'getting strings from {len(instructions)} elements')

        strings_from_elements = []

        for instruction in instructions:
            string_from_element = self.get_string_from_element(instruction)
            result = Result(instruction=instruction, string=string_from_element)

            strings_from_elements.append(result)

        return strings_from_elements

    def get_string_from_one_of_elements(self, instructions: list[SimpleInstruction]):
        self.__logger.info(f'getting string from one of {len(instructions)} elements')

        result = None

        for instruction in instructions:
            try:
                self.__logger.info(f'trying to get string from {instruction.element['name']}')

                Result = namedtuple('Result', ['instruction', 'string'])
                string_from_element = self.get_string_from_element(instruction)
                result = Result(instruction=instruction, string=string_from_element)

                break

            except Exception:
                self.__logger.warning(f'failed to get string from {instruction.element['name']}')

        if result is None:
            self.__logger.error('failed to get string from any elements')

            raise ValueError('failed to get string from any elements')

        self.__logger.info(f'string from {result.instruction.element['name']}: {result.string}')

        return result

    def quit(self):
        self.__logger.info(f'terminating web robot - {self.name}')
        self.__driver.quit()
