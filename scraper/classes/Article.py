class Article:
    def __int__(self, **kwargs):
        if 'link' in kwargs:
            self.link = kwargs['link']
        else:
            raise Exception("Link cannot be empty.")

        if 'header' in kwargs:
            self.header = kwargs['header']
        else:
            self.header = ""

        if 'description' in kwargs:
            self.description = kwargs['header']
        else:
            self.description = ""

        if 'category' in kwargs:
            self.category = kwargs['category']
        else:
            self.category = ""

        if 'author' in kwargs:
            self.author = kwargs['author']
        else:
            self.author = ""

        if 'published_at' in kwargs:
            self.published_at = kwargs['published_at']
        else:
            self.published_at = ""

        if 'modified_at' in kwargs:
            self.modified_at = kwargs['modified_at']
        else:
            self.modified_at = ""

        if 'paragraphs' in kwargs:
            self.paragraphs = kwargs['paragraphs']
        else:
            self.paragraphs = ""

        if 'comments' in kwargs:
            self.comments = kwargs['comments']
        else:
            self.comments = []