import os
import json
import feedparser
from logger import get_logger
from newsItem import NewsItem
import gpt
import notification

log = get_logger('newstrum')

rss_feeds_string = os.getenv("rss_feeds", "")
RSS_FEEDS = json.loads(rss_feeds_string)

def fetch_rss(rss_link: str):
    news_items = []

    feed = feedparser.parse(rss_link)

    for entry in feed.entries:
        title = entry.title
        link = str(entry.link).replace('&sourceType=rss', '') if 'sourceType=rss' in entry.link else entry.link
        
        item = NewsItem(title=title, link=link)
        news_items.append(item)

    return news_items


def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

if __name__ == "__main__":
    for rss_category, rss_link in RSS_FEEDS.items():
        news_items = fetch_rss(rss_link)
        log.info(f"📌 [{rss_category}]: {len(news_items)}개 수집 완료")

        for idx, chunk in enumerate(chunk_list(news_items[:20], 5), start=1):
            news_text = '\n'.join(news.getString() for news in chunk)
            prompt = f"""
            다음은 최근 뉴스 링크입니다.

            {news_text}

            위 뉴스들을 참고해서 요약해주세요.

            요구 사항:
            1. 어떤 이슈들이 다뤄지고 있는지 요약해 주세요.
            2. 경제나 사회에 어떤 영향을 줄 것인지 예측해주세요.
            3. 향후 경제 분석 및 전망을 간략히 알려 주세요.
            4. 투자 의견이 있다면 알려주세요.
            """
            result = f'```{gpt.analyze(prompt=prompt)}```'.replace("\n", "\n\n")
            notification.send_to_discord(f'[{rss_category}]\n{result}')
            notification.send_to_hangout(f'[{rss_category}]\n{result}')