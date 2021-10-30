import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import generic



from .models import Message, Question, Choice

class IndexView(generic.ListView):
    template_name = 'messages/index.html'
    context_object_name = 'latest_messages_list'

    def get_queryset(self):
        
        return Message.objects.all()
    


def addView(request):
    Message.objects.create(message_from = request.user, message_text = request.POST.get('content'), pub_date = '1996-12-21')
    
    return redirect('/') 


    


class DetailView(generic.DetailView):
    model = Question
    template_name = 'messages/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'messages/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'messages/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('messages:results', args=(question.id,)))