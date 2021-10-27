from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login
from .models import Choice, Question, Vote
from utils import create_user


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
        return render(request, 'polls/results.html', {'question': question})
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
        user_vote = Vote.objects.filter(user=request.user).filter(choice__question=question)
        if len(user_vote) == 0:
            user_vote = Vote(user=request.user, choice=selected_choice)
        else:
            user_vote = user_vote[0]
            user_vote.change_vote(new_choice=selected_choice)
        user_vote.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST["email"]
        password = request.POST["password"]
        create_user(
            username=username,
            email=email,
            password=password
        )
        # success fully create new user and redirect
        login(request, user=username, password=password)
        return redirect('login')
    return render(request, 'polls/register.html')
