from django.shortcuts import render
from account.forms import UserCreationForm, UserLoginForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from .model_form import CreateQuestion, CreateAnswerForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import Question , Answer
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

User = get_user_model()

def home(request):
    questions = Question.objects.all().order_by('-id')

    # Show 10 contacts per page.
    paginator = Paginator(questions, 3) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {
        'page_obj': page_obj,
        'number_of_questions': Question.objects.count(),
        'user_uuid': str(request.user.pk)
    })


def signUP(request):
    if request.method == 'POST' :
        forms = UserCreationForm(request.POST)

        if forms.is_valid() :
            users = forms.save()
            return render(request, 'success.html' , {
                'user_obj': users
            })

    else :
        forms = UserCreationForm()

    return render(request, 'registration/signup.html' , {
        'generateForm' : forms
    })

@staff_member_required(login_url='restrict')
def addQuestion(request) :
    if request.method == 'POST' :
        add = CreateQuestion(request.POST)
        if add.is_valid() :
            add.save()
            return render(request , 'QuestionForm.html' , {
                'question_addition_status' : True
            })
    else :
        add = CreateQuestion()

    return render(request , 'QuestionForm.html' , {
        'renderForm' : add,
        'add_btn': True
    })

def unauthorisedAccess(request) :
    return render(request , 'alert.html')


@staff_member_required(login_url = 'restrict')
def updateQuestion(request , question_id) :
    question_id = int(question_id)

    try :
        question_selected = Question.objects.get(id = question_id)
    except Question.DoesNotExist:
        return redirect('home')

    UpdateQuestion = CreateQuestion(request.POST or None, instance = question_selected)

    if UpdateQuestion.is_valid():
        UpdateQuestion.save()
        return render(request , 'QuestionForm.html', {
            'update_question_status': True
        })

    else :
        UpdateQuestion = CreateQuestion(request.POST or None, instance = question_selected)

    return render(request , 'QuestionForm.html' , {
        'renderForm' : UpdateQuestion,
        'update_btn': True

    })

def answerQuestion(request , question_id):
    question = Question.objects.get(pk=question_id).question
    if request.method == 'POST':
        form = CreateAnswerForm(request.POST)
        if form.is_valid:
            username = request.user.username

            answer = Answer.objects.create(user=User.objects.get(username=username), question=Question.objects.get(pk=question_id), answer=form.data['answer'])
            answer.save()

            return render(request, 'answerForm.html' , {
                'tag' : 'Answer Submitted!',
                'answered': True
            })
    else:
        form = CreateAnswerForm()

    return render(request , 'answerForm.html' , {
        'renderForm' : form,
        'question_name': question
    })


def delete_question(request, question_id):
    question_id = int(question_id)

    try :
        question_selected = Question.objects.get(id = question_id)
        question_selected.delete()

        return render(request, 'deleted_alert.html')

    except Question.DoesNotExist:
        return redirect('home')



def list_students(request, lecturer_id):

    students = []
    for user in User.objects.all():
        if not user.is_staff:
            students.append(user)

    # Show 10 contacts per page.
    paginator = Paginator(students, 10) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'student_list.html', {'page_obj': page_obj})


def student_answers(request, lecturer_id, student_clicked):
    student = User.objects.get(pk=student_clicked)
    answers_of_student = Answer.objects.filter(user=student)

    return render(request, 'student_answers.html', {
        'answers': answers_of_student,
        'student': student,
        'count': answers_of_student.count(),
        'questions_count': Question.objects.count()
    })
