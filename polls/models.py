import datetime
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        now = timezone.now()
        return self.is_published() and now <= self.end_date

    def __str__(self):
        return self.question_text

    # admin customizations
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    is_published.boolean = True
    is_published.short_description = 'Is published?'
    can_vote.boolean = True
    can_vote.short_description = 'Can vote?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        count = Vote.objects.filter(choice=self).count()
        return count

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    @property
    def question(self):
        return self.choice.question

    def change_vote(self, new_choice):
        self.choice = new_choice

    def __str__(self):
        return f"({self.user.username}) vote ({self.choice}) for ({self.question})"
