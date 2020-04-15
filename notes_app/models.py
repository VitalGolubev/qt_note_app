class Note:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.title = kwargs.get("title", "")
        self.content = kwargs.get("content", "")

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Note id={self.id} title={self.title}>"