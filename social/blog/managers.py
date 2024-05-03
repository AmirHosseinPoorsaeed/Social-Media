from django.db.models import Manager


class PostManager(Manager):
    def active(self):
        return self.filter(active=True)
