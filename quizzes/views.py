from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.http import JsonResponse
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import QuizForm, QuestionForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.forms import inlineformset_factory

def send_email(user, email_type, mail_subject, template):
    message = render_to_string(template, {
        'user': user,
        'type': email_type,
    })
    from_email = "JEOPARDY <moinaAkhanda@gmail.com>"
    send_email = EmailMultiAlternatives(mail_subject, '', to=[user.email], from_email=from_email, reply_to=[from_email])
    send_email.attach_alternative(message, 'text/html')
    

def home(request):
    quiz = Quiz.objects.all()
    para = {'quiz' : quiz}
    return render(request, "home.html", para)

@login_required(login_url = '/login')
def quiz(request, myid):
    quiz = Quiz.objects.get(id=myid)
    return render(request, "quiz.html", {'quiz':quiz})



def quiz_data_view(request, myid):
    quiz = get_object_or_404(Quiz, id=myid)
    questions = []
    for q in quiz.get_questions():
        answers = [a.content for a in q.get_answers()]
        questions.append({str(q): answers})

    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


def save_quiz_view(request, myid):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(content=k)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(id=myid)

        score = 0
        marks = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.content)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.content:
                        if a.correct:
                            score += 1
                            correct_answer = a.content
                    else:
                        if a.correct:
                            correct_answer = a.content

                marks.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                marks.append({str(q): 'not answered'})
     
        Marks_Of_User.objects.create(quiz=quiz, user=user, score=score)
        
        return JsonResponse({'passed': True, 'score': score, 'marks': marks})
    

def add_quiz(request):
    if request.method == "POST":
        form = QuizForm(data=request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            # Ensure you're setting the category field
            quiz.category = form.cleaned_data['category']
            quiz.save()
            obj = form.instance
            return render(request, "add_quiz.html", {'obj': obj})
    else:
        form = QuizForm()
    return render(request, "add_quiz.html", {'form': form})



def add_question(request):
    questions = Question.objects.all()
    questions = Question.objects.filter().order_by('-id')
    if request.method=="POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "add_question.html")
    else:
        form=QuestionForm()
    return render(request, "add_question.html", {'form':form, 'questions':questions})

def delete_question(request, myid):
    question = Question.objects.get(id=myid)
    if request.method == "POST":
        question.delete()
        return redirect('/add_question')
    return render(request, "delete_question.html", {'question':question})

def delete_result(request, result_id):
    result = get_object_or_404(Marks_Of_User, pk=result_id)
    result.delete()
    return redirect('home')
# def results(request):
#     marks = Marks_Of_User.objects.all()
#     return render(request, "results.html", {'marks':marks})
def results(request):
    marks = Marks_Of_User.objects.all()
    for mark in marks:
        user = mark.user
        email_type = 'quiz_results'
        mail_subject = 'Quiz Results'
        template = 'email.html'
        send_email(user, email_type, mail_subject, template)

    return render(request, "results.html", {'marks': marks})
