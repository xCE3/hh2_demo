from django.shortcuts import render, redirect

from .models import *
from django.contrib import messages
# from datetime import datetime
import bcrypt

# Create your views here.
def current_user(request):
	return User.objects.get(id = request.session['user_id'])

def index(request):
    return render(request, 'handyhelper2_app/index.html')

def register(request):
	check = User.objects.validateUser(request.POST)
	if request.method != 'POST':
		return redirect('/')
	if check[0] == False:
		for error in check[1]:
			messages.add_message(request, messages.INFO, error, extra_tags="registration")
			return redirect('/')
	if check[0] == True:
		#has password
		hashed_pw = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt())

		#create user
		user = User.objects.create(
			name = request.POST.get('name'),
			alias = request.POST.get('alias'),
			email = request.POST.get('email'),	
			password = hashed_pw,
			birthdate = request.POST.get('birthdate')
		)

		#add user to session, logging them in
		request.session['user_id'] = user.id
		#route to jobs page
		return redirect('/dashboard')

def login(request):
	if request.method != 'POST':
		return redirect('/')
	#find user
	user = User.objects.filter(email = request.POST.get('email')).first()

	#Check user credentials
	#add them to session and log in or add error message and route to home page
	if user and bcrypt.checkpw(request.POST.get('password').encode(), user.password.encode()):
		request.session['user_id'] = user.id
		return redirect('/dashboard')
	else: 
		messages.add_message(request, messages.INFO, 'invalid credentials', extra_tags="login")
		return redirect('/')
	return redirect('/dashboard')

def logout(request):
		request.session.clear()
		return redirect('/')

def dashboard(request):
    context = {
    'jobs' : Job.objects.all()
    }
    return render(request, "handyhelper2_app/jobs.html", context)

def new(request):
    return render(request, "handyhelper2_app/new.html")

def edit(request, id):

    context = {
    'job' : Job.objects.get(id=id)
    }
    
    return render(request, "handyhelper2_app/edit.html", context)

def display(request, id):

    context = {
    'job' : Job.objects.get(id=id)
    }
    return render(request, "handyhelper2_app/job.html", context)


def job_user(request, id):

	user =  User.objects.get(id = id)
	context = {
		'user': user,
		'likes': user.likes.all()		
	}
	return render(request, 'handyhelper2_app/user.html', context)

def create(request):
    #validate data
    errors = Job.objects.validate(request.POST)
    if (errors):
        print ("==== errror ")
        for error in errors:
            messages.error(request, errors[error])
        print (messages)
        return redirect("/new")
    print ("===== no errors ===")
    Job.objects.create(job=request.POST['job'], location=request.POST['location'], releasedate=request.POST['releasedate'])
    return redirect("/dashboard")

def update(request):
    print ("------update")
    # validate data
    errors = Job.objects.validate(request.POST)
    if (errors):
        print ("==== errror ")
        for error in errors:
            messages.error(request, errors[error])
        print (messages)
        reURL = "/jobs/"+ str(request.POST['id']) + "/edit"
        return redirect(reURL)
    u = Job.objects.get(id=request.POST['id'])
    u.job = request.POST['job']
    u.location = request.POST['location']
    u.releasedate = request.POST['releasedate']
    u.save()
    return redirect("/"+str(u.id))