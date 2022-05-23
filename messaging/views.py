import datetime
from email import message
from getpass import getuser

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.views import generic





from .models import Message, Question, Choice

class IndexView(generic.ListView):
    template_name = 'messages/index.html'
    context_object_name = 'latest_messages_list'


    

    

    def get_queryset(self):
        
        allMessages = Message.objects.all()
        messages = []
        for mes in allMessages:
            messages.append(mes.message_text)

        
        return messages
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        allMessages = Message.objects.all()
        User = get_user_model()
       
        messages = []
        
        for mes in allMessages:
           
            try:
                messages.append((mes.message_text,User.objects.get(username = mes.message_from)))
            except User.DoesNotExist:
                messages.append((mes.message_text,"AnonymousUser"))
            
            
                
        messages.reverse()
        context['messages'] = messages
        
        
        context['latest_messages_list'] = messages[0:5]

       
        
        
        return context
    


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


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        
        form = UserCreationForm()
    return render(request, 'messages/signup.html', {'form': form})

class userView(generic.DetailView):

    template_name = 'messages/userInfo.html'

    def get_context_data(self, **kwargs):
        context = super(userView, self).get_context_data(**kwargs)
        User = get_user_model()
        allMessages = Message.objects.all()
        
        userId = self.kwargs['pk']
       
        usersMessages = []
        user = User.objects.get(pk=userId)

        for mes in allMessages:

           if mes.message_from == user.username:
               usersMessages.append(mes.message_text)

        print(usersMessages)
        context['viewedUser'] = user
        context['messagesByUser'] = usersMessages
        
        return context

    def get_queryset(request):
        
        allMessages = Message.objects.all()
        

        
        return allMessages
    
  
     
  
