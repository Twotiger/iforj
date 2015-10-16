from django.db import models
from qa.models import User

class Bigsmall(models.Model):
    user_id = models.ForeignKey(User, related_name="game_user")
    times = models.PositiveSmallIntegerField(default=1000)
    money = models.IntegerField(default=1000)

    class Meta:
        ordering = ('-money',)

    def __unicode__(self):
        return  self.user_id.name