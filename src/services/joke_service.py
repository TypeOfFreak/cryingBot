from src import models


class JokeService:
    def __init__(self, session):
        self.session = session

    def save_joke(self, text, image=None):
        fun = models.Joke(text=text, image=image)
        self.session.add(fun)
        self.session.commit()

    def get_jokes(self):
        return self.session.query(models.Joke).all()
