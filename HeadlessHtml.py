from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
from pathlib import Path
import time


class KugouSpider:
    WEB_URL = "http://www.kugou.com/"
    # WEB_URL = "http://www.kugou.com/yy/special/single/378394.html"
    SAVE_PATH = "E:/KG/Music/"

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        self.browser = webdriver.Chrome(chrome_options=chrome_options)

        self.save_path = Path(KugouSpider.SAVE_PATH)
        if not self.save_path.exists():
            self.save_path.mkdir(parents=True)

    def run(self):
        self.get_songs(self.get_urls())

    def get_urls(self):
        self.browser.get(KugouSpider.WEB_URL)
        li_items = self.browser.find_elements_by_xpath("//li[@data]/a")
        song_urls = [li.get_attribute("href") for li in li_items]
        wait = WebDriverWait(self.browser, 10)
        # li_items = browser.find_elements_by_xpath("//li/a[@href=\"javascript:;\"]")
        # song_urls = ["http://www.kugou.com/song/#hash={0}".format(li.get_attribute("data").split('|')[0])
        #              for li in li_items]
        return song_urls

    def get_songs(self, song_urls):
        for url in song_urls:
            print("request url:{0}".format(url))
            # browser.implicitly_wait(10)
            # browser.set_page_load_timeout(10)
            self.browser.get(url)
            time.sleep(2)
            self.browser.refresh()
            time.sleep(3)
            try:
                # song_name = wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "change-time"), "00:01"))
                song = self.browser.find_element_by_id("songName")
                player = self.browser.find_element_by_id("myAudio")
                song_url = player.get_attribute("src")
                if song and song.text == "酷狗音乐":
                    continue
                if song_url:
                    print(song.text, song_url)
                    req = requests.get(song_url)
                    song_path = self.save_path / (song.text + ".mp3")
                    with song_path.open(mode="wb") as f:
                        f.write(req.content)
                        print("---> Save song : {0}".format(song_path))
            except(TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
                print(e.msg)

        self.browser.quit()


class KugouSearchSpider(KugouSpider):
    WEB_URL = "http://www.kugou.com/yy/html/search.html#searchType=song&searchKeyWord="

    # WEB_URL = "http://www.kugou.com/"

    def __init__(self, keyword="抖音"):
        super().__init__()
        self.keyword = keyword

    def run(self):
        self.get_songs(self.get_urls())

    def get_urls(self):
        self.browser.get(KugouSearchSpider.WEB_URL + self.keyword)
        # li_items = self.browser.find_elements_by_xpath("//li[@class=\"clearfix\"]/a")
        li_items = self.browser.find_elements_by_xpath("//a[@class=\"album_name\"]")
        album_urls = [li.get_attribute("href") for li in li_items]
        song_urls = []
        for url in album_urls:
            self.browser.get(url)
            song_a = self.browser.find_elements_by_xpath("//ul[@class=\"songList\"]/li[1]/a")[0]
            token = song_a.get_attribute("data").split("|")[0]
            song_urls.append("http://www.kugou.com/song/#hash={0}".format(token))
        return song_urls

    def get_songs(self, song_urls):
        for url in song_urls:
            print("request url:{0}".format(url))
            # browser.implicitly_wait(10)
            # browser.set_page_load_timeout(10)
            self.browser.get(url)
            time.sleep(2)
            self.browser.refresh()
            time.sleep(3)
            try:
                # song_name = wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "change-time"), "00:01"))
                song = self.browser.find_element_by_id("songName")
                player = self.browser.find_element_by_id("myAudio")
                song_url = player.get_attribute("src")
                if song and song.text == "酷狗音乐":
                    continue
                if song_url:
                    print(song.text, song_url)
                    req = requests.get(song_url)
                    song_path = self.save_path / (song.text + ".mp3")
                    with song_path.open(mode="wb") as f:
                        f.write(req.content)
                        print("---> Save song : {0}".format(song_path))
            except(TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
                print(e.msg)

        self.browser.quit()


if __name__ == "__main__":
    # spider = KugouSpider()
    spider = KugouSearchSpider("冯提莫")
    spider.run()
