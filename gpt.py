from logger import get_logger
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

log = get_logger('GPT')

def setup():
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=chrome")
    options.add_argument("profile-directory=Default")
    options.add_argument('remote-debugging-port=9999')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')

    return webdriver.Chrome(options=options)

def analyze(prompt:str):
    log.info("ai 페이지 접근 중...")
    try:
        driver = setup()
        driver.get('https://wrtn.ai')
        sleep(2)
        ad_close_button = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div/div/div/div[2]/div/button[1]')
        if ad_close_button:
            ad_close_button[1].click()

        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rich-textarea"]')))
        input_box = driver.find_element(By.XPATH, '//*[@id="rich-textarea"]')
        input_box.clear()
        input_box.send_keys(prompt)
        input_box.send_keys(Keys.ENTER)
        log.info("분석 중...")
        sleep(30)

        return driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[2]/div/div/div/div[1]/div/div/div/div/div[1]/div/div/div/div[3]/div/div[1]/div[1]/div[3]/div[2]/div').text
    finally:
        driver.quit()