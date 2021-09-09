import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question

def create_question(question_text, days, active_interval=1):
    """Create a question object

    Args:
        question_text: the question text
        days: published offset to now (negative for questions published 
            in the past, positive for questions that have yet to be published).
        active_interval: lenght of active question from start_date to end_date

    Returns:
        a question object with question text, start date and end date
    """
    start = timezone.now() + datetime.timedelta(days=days)
    end = start + datetime.timedelta(days=active_interval)
    print(type(start), type(end))
    return Question.objects.create(question_text=question_text, pub_date=start, end_date=end)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_ended_question(self):
        """
        Questions with a end_date in the past are displayed on the
        index page but can't vote.
        """
        create_question(question_text="Ended question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Ended question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_ended_question(self):
        """
        Even if both ended and future questions exist, but future question
        is not display
        """
        create_question(question_text="Ended question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'], 
            ['<Question: Ended question.>'])

    def test_two_active_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Active question 1.", days=-10, active_interval=20)
        create_question(question_text="Active question 2.", days=-1, active_interval=10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Active question 2.>', '<Question: Active question 1.>']
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 302 found (redirect to index)
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5, active_interval=10)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)