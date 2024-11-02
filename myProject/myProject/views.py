from django.shortcuts import render,redirect

from myApp.models import *
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def signupPage(request):
    
    if request.method=='POST':
        
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        Confirm_password=request.POST.get("Confirm_password")
        user_type=request.POST.get("user_type")
        Profile_Pic=request.FILES.get("Profile_Pic")
        display_name=request.POST.get("display_name")
    
        
        if password==Confirm_password:
            
            
            user=customUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type=user_type,
                Profile_Pic=Profile_Pic,
                display_name=display_name,
            )
            if user_type=='seeker':
                seekerProfileModel.objects.create(user=user)
                
            elif user_type=='recruiter':
                recruiterProfileModel.objects.create(user=user)
            
            return redirect("signInPage")
            
    return render(request,"signupPage.html")


def signInPage(request):
    if request.method == 'POST':
        
        user_name=request.POST.get("username")
        pass_word=request.POST.get("password")

        try:
            user = authenticate(request, username=user_name, password=pass_word)

            if user is not None:
                login(request, user)
                return redirect('homePage') 
            else:
                return redirect('signInPage')

        except customUser.DoesNotExist:
            return redirect('signInPage')

    return render(request, 'signInPage.html')

@login_required
def homePage(request):

    total_jobs=JobModel.objects.all().count()
    total_applications=jobApplyModel.objects.all().count()
    total_users=customUser.objects.all().count()

    context={
        'total_jobs':total_jobs,
        'total_applications':total_applications,
        'total_users':total_users
    }
    
    
    return render(request,"homePage.html",context)


def logoutPage(request):
    
    logout(request)
    
    return redirect('signInPage')

@login_required
def profilePage(request):
    
    return render(request,"profilePage.html")


@login_required
def addJobPage(request):

    current_user=request.user
    if current_user.user_type == "recruiter":
        if request.method=="POST":
            jobs=JobModel()
            jobs.user=current_user
            jobs.job_title=request.POST.get("job_title")
            jobs.number_of_openings=request.POST.get("number_of_openings")
            jobs.skills=request.POST.get("skills")
            jobs.category=request.POST.get("category")
            jobs.description=request.POST.get("description")
            jobs.job_Pic=request.FILES.get("job_Pic")
            
            jobs.save()
           
            return redirect("jobFeed")
    
    return render(request,"addJobPage.html")

@login_required
def createdJobPage(request):

    current_user=request.user
    jobs=JobModel.objects.filter()

    context= {
        'jobs': jobs
    }
    
    return render(request,"createdJobPage.html",context)

@login_required
def jobFeed(request):

    current_user=request.user
    jobs=JobModel.objects.all()

    context= {
        'jobs': jobs
    }
    
    return render(request,"jobFeed.html",context)

@login_required
def deleteJob(request,job_id):

    jobs=JobModel.objects.filter(id=job_id)
    jobs.delete()

    
    return redirect("createdJobPage")


@login_required
def viewJOb(request,job_id):

    jobs=JobModel.objects.filter(id=job_id)

    context= {
        'jobs': jobs
    }
    
    
    return render(request,"viewJOb.html",context)

@login_required
def editJob(request,job_id):

    jobs=JobModel.objects.get(id=job_id)

    context= {
        'jobs': jobs
    }

    current_user=request.user
    if current_user.user_type == "recruiter":
        if request.method=="POST":
            jobs=JobModel()
            jobs.id=request.POST.get("job_id")
            jobs.user=current_user
            jobs.job_title=request.POST.get("job_title")
            jobs.number_of_openings=request.POST.get("number_of_openings")
            jobs.skills=request.POST.get("skills")
            jobs.category=request.POST.get("category")
            jobs.description=request.POST.get("description")
            jobs.job_Pic=request.FILES.get("job_Pic")
            
            jobs.save()
           
            return redirect("createdJobPage")
    
    return render(request,"editJob.html",context)

@login_required
def applyJob(request,job_id):


    job=JobModel.objects.get(id=job_id)
    applied_jobs=jobApplyModel.objects.filter(user=request.user, job=job)

    context= {
        'jobs': job,
        'applied_jobs': applied_jobs
    }

    current_user=request.user
    
    if current_user.user_type == 'seeker':
        
        
        if request.method=='POST':
            
            Resume=request.FILES.get("Resume")
            Cover=request.POST.get("Cover")
            Skills=request.POST.get("Skills")
            image=request.FILES.get("image")
            
            apply=jobApplyModel(
                user=current_user,
                job=job,
                Resume=Resume,
                Cover=Cover,
                Skills=Skills,
                image=image,
                
            )
            apply.save()
            return redirect("appliedJob")
    
    
    return render(request,"applyJob.html",context)

@login_required
def searchJob(request):
    
    query = request.GET.get('query')
    
    if query:
        
        jobs = JobModel.objects.filter(Q(job_title__icontains=query) 
                                       |Q(skills__icontains=query) 
                                       |Q(category__icontains=query) 
                                       )
    
    else:
        jobs = JobModel.objects.none()
        
    context={
        'jobs':jobs,
        'query':query
    }
    
    return render(request,"searchJob.html",context)

@login_required
def skillMatchingPage(request):
    
    user=request.user
    
    mySkill=user.seekerProfile.skills
    jobs=JobModel.objects.filter(skills=mySkill)
    context={
        'jobs':jobs
    }
    print(mySkill)
    
    return render(request,"skillMatchingPage.html",context)

@login_required
def appliedJob(request):
    current_user = request.user

    
    job_applications = jobApplyModel.objects.filter(user=current_user)

    context = {
        "Job": job_applications, 
    }
    return render(request, "appliedJob.html", context)


@login_required
def editProfilePage(request):
    
    
    
    current_user=request.user
    
    if request.method=='POST':
        current_user.username=request.POST.get("username")
        current_user.first_name=request.POST.get("first_name")
        current_user.last_name=request.POST.get("last_name")
        current_user.email=request.POST.get("email")
        current_user.job_id=request.POST.get("job_id")
        skill = request.POST.get('skills')
        if request.FILES.get("profile_pic"):
            current_user.Profile_Pic=request.FILES.get("profile_pic")
        current_user.display_name=request.POST.get("display_name")
    
            
        try:
            seekerProfile=seekerProfileModel.objects.get(user=current_user)
            seekerProfile.skills = skill
            seekerProfile.save()
            current_user.save()
            
            return redirect("profilePage")
            
        except seekerProfileModel.DoesNotExist:
            seekerProfile=None
            
        try:
            recruiterProfile=recruiterProfileModel.objects.get(user=current_user)
            
            recruiterProfile.Company_name=request.POST.get("Company_name")
            recruiterProfile.save()
            current_user.save()
            
            return redirect("profilePage")
            
        except recruiterProfileModel.DoesNotExist:
            recruiterProfile=None
    
    return render(request, "editProfilePage.html")

