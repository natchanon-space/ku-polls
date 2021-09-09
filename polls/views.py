from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question


def index(request):
    # get list of can_vote questions
    active_question_ids = []
    for question in Question.objects.all():
        if question.is_published():
            active_question_ids.append(question.id)
    questions = Question.objects.filter(
        id__in=active_question_ids
    ).order_by('-pub_date')
    context = {'latest_question_list': questions}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if question.can_vote():
        return render(request, 'polls/detail.html', {'question': question})
    else:
        messages.error(request, f'Sorry, voting for Question {question_id} is not allowed')
        return redirect('polls:index')


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if question.is_published():
        return render(request, 'polls/results.html', {'question': question })
    else:
        messages.error(request, f'Sorry, Question {question_id} not published yet')
        return redirect('polls:index')


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        # save in data base
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
