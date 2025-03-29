# Web Robota

쉽게 사용 할 수 있는 웹 자동화 모듈

## 개요
Web Robota는

웹에 대해 깊은 이해가 없어도 쉽게 웹에서 원하는 정보를 수집하거나

웹 사이트에 대한 자동화를 수행하는 스크립트를 작성할 수 있게 도와주는 Python 모듈입니다.

## 사용 방법

```python
from web_robota import WebRobota, WebElement, SimpleInstruction

# WebElement 정의
SAMPLE_ELEMENT = WebElement(name='sample_1', xpath='/html/body/div[1]/div[1]/div[3]')

# 타겟 URL
URL = 'www.naver.com'

if __name__ == '__main__':
    robota = WebRobota()
    
    # 옵션 설정
    robota.option_builder.set_headless() # GUI 없이 크롤러 구동
    robota.option_builder.set_disable_gpu() # GPU 사용 해제
    robota.option_builder.set_no_sandbox() # Sandbox 모드 해제
    robota.option_builder.set_download_path('./downloads') # 다운로드 경로 설정
    robota.option_builder.set_notifications(True) # 알림 허용 여부 설정
    robota.option_builder.set_allow_multiple_downloads(True) # 여러 파일 다운로드 허용 여부 설정
    robota.option_builder.set_prompt_for_download(False) # 다운로드 프롬프트 표시 여부 설정
    
    robota.boot_up() # Web Robota 시작

    robota.go_to(URL) # URL 이동
    robota.click(SimpleInstruction(element=SAMPLE_ELEMENT, timeout=1)) # 특정 요소 click하기
    
```