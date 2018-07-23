from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
from pathlib import Path
import time

WEB_URL = "http://www.kugou.com/"
# WEB_URL = "http://www.kugou.com/yy/special/single/378394.html"
SAVE_PATH = "E:/KG/Music/"

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
browser = webdriver.Chrome(chrome_options=chrome_options)

p = Path(SAVE_PATH)
if not p.exists():
    p.mkdir(parents=True)

browser.get(WEB_URL)
li_items = browser.find_elements_by_xpath("//li[@data]/a")
song_urls = [li.get_attribute("href") for li in li_items]
wait = WebDriverWait(browser, 10)
# li_items = browser.find_elements_by_xpath("//li/a[@href=\"javascript:;\"]")
# song_urls = ["http://www.kugou.com/song/#hash={0}".format(li.get_attribute("data").split('|')[0])
#              for li in li_items]

for url in song_urls:
    print("request url:{0}".format(url))
    # browser.implicitly_wait(10)
    # browser.set_page_load_timeout(10)
    browser.get(url)
    time.sleep(2)
    browser.refresh()
    time.sleep(3)
    try:
        # song_name = wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "change-time"), "00:01"))
        song = browser.find_element_by_id("songName")
        player = browser.find_element_by_id("myAudio")
        song_url = player.get_attribute("src")
        if song and song.text == "酷狗音乐":
            continue
        if song_url:
            print(song.text, song_url)
            req = requests.get(song_url)
            song_path = p / (song.text + ".mp3")
            with song_path.open(mode="wb") as f:
                f.write(req.content)
                print("---> Save song : {0}".format(song_path))
    except(TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
        print(e.msg)

browser.quit()
