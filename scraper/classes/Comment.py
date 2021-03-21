class Comment:
    def __init__(self, **kwargs):
        if 'author_text' in kwargs:
            split_author_text = kwargs['author_text'].split(',')

            self.author = split_author_text[0]
            self.city = split_author_text[1]
        else:
            raise Exception("Author_text cannot be empty.")

        if 'text' in kwargs:
            self.text = kwargs['text']
        else:
            raise Exception("Text cannot be empty.")

        if 'likes' in kwargs:
            self.likes = int(kwargs['likes'][1:])
        else:
            raise Exception("Likes cannot be empty.")

        if 'dislikes' in kwargs:
            self.dislikes = int(kwargs['dislikes'][1:])
        else:
            raise Exception("Dislikes cannot be empty.")

        if 'time' in kwargs:
            self.time = kwargs['time']
        else:
            raise Exception("Time cannot be empty.")

        # TODO -> calculate ratio between likes and dislikes
