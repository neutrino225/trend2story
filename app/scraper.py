import time
import logging
import asyncio
from gnews import GNews
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logging.getLogger("WDM").setLevel(logging.NOTSET)

class TrendScraper:
    def __init__(self):
        pass 
    
    def _setup_driver(self):
        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--headless")
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    async def get_google_trends(self):
        try:
            driver = self._setup_driver()
            driver.get("https://trends.google.com/trending?geo=PK")
            await asyncio.sleep(5)

            trends = driver.find_elements(By.CLASS_NAME, "mZ3RIc")
            trend_list = [trend.text for trend in trends if trend.text]

        finally:
            driver.quit()
        return trend_list

    async def get_youtube_trends(self):
        try:
            driver = self._setup_driver()
            driver.get("https://www.youtube.com/feed/trending")
            await asyncio.sleep(5)
            driver.execute_script("window.scrollTo(0, 2000)")
            await asyncio.sleep(2)

            videos = driver.find_elements(
                By.CSS_SELECTOR, "ytd-video-renderer, ytd-grid-video-renderer"
            )
            titles = []
            for video in videos:
                try:
                    title = video.find_element(By.CSS_SELECTOR, "#video-title").text
                    if title:
                        titles.append(title)
                except Exception:
                    continue
        finally:
            driver.quit()
        return titles

    async def get_news_trends(self):
        news_client = GNews(language="en", period="24h")
        news = news_client.get_top_news()
        return [item["title"] for item in news if "title" in item]

    async def get_trends(self, source) -> str:
        source = source.lower()
        try:
            if source == "google":
                trends = await self.get_google_trends()
            elif source == "youtube":
                trends = await self.get_youtube_trends()
            elif source == "news":
                trends = await self.get_news_trends()
            else:
                raise ValueError(f"Unknown trend source: {source}")
        except Exception as e:
            return f"Error fetching trends from {source}: {str(e)}"

        return "\n".join(trends)
