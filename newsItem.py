class NewsItem:
    def __init__(self, title, link):
        self.title = title
        self.link = link

    def getString(self):
        return f'`{self.title}`(`{self.link}`)'