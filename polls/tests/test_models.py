import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_on_time_question(self):
        """
        is_published() return True for question whose pub_date
        is equal or less than current time
        """
        time = timezone.now()
        on_time_quesiton = Question(pub_date=time)
        self.assertIs(on_time_quesiton.is_published(), True)

    def test_is_published_with_future_quesiton(self):
        """
        is_published() return False for quesiton whose pub_date
        is in the future
        """
        time = timezone.now() + datetime.timedelta(seconds=5)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with_old_question(self):
        """
        is_published() return True for question whose pub_date
        is in the past
        """
        time = timezone.now() - datetime.timedelta(seconds=5)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.is_published(), True)

    def test_can_vote_with_future_question(self):
        """
        can_vote() return False for question whose pub_date
        is in the future or not publish yet
        """
        pub_date = timezone.now() + datetime.timedelta(minutes=5)
        end_date = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(future_question.can_vote(), False)

    def test_can_vote_with_active_question(self):
        """
        can_vote() return True for question whose published and
        within end_date
        """
        pub_date = timezone.now()
        end_date = timezone.now() + datetime.timedelta(days=1)
        active_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(active_question.can_vote(), True)

    def test_can_vote_with_ended_question(self):
        """
        can_vote() return False for question whose end_date
        is more than the current time
        """
        pub_date = timezone.now()
        end_date = timezone.now() - datetime.timedelta(minutes=5)
        ended_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(ended_question.can_vote(), False)
