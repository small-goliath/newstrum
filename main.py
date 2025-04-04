import os
import feedparser
import logging
import logging.config
from newsItem import NewsItem
import gpt
import notification

logging.config.fileConfig('logging.conf')
log = logging.getLogger('newstrum')

rss_feed_string = os.getenv("rss_feeds", "")
RSS_FEEDS = [url.strip() for url in rss_feed_string.split(",") if url.strip()]

def fetch_rss():
    news_items = []

    for link in RSS_FEEDS:
        feed = feedparser.parse(link)

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
    news_items = fetch_rss()
    result = []
    log.info(f"📌 {len(news_items)}개 수집 완료")

    try:
        for idx, chunk in enumerate(chunk_list(news_items[:10], 5), start=1):
            news_text = '\n'.join(news.getString() for news in chunk)
            prompt = f"""
            다음은 최근 뉴스 링크입니다. (파트 {idx})

            {news_text}

            위 뉴스들을 참고분석하고:
            1. 어떤 이슈들이 다루어지고 있는지 요약해 주세요.
            2. 향후 경제에 대한 분석과 전망을 알려 주세요.
            """
            result.append(gpt.analyze(prompt=prompt))
    finally:
        message = "\n\n".join(map(str, result))
        notification.send_to_discord(message)
        notification.send_to_hangout(message)