from email import message
from . import check
from distutils.command.upload import upload
from django.shortcuts import render
from django.http import HttpResponse
from .models import Resume, Contact
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from recruiter.models import selectedResume

def index(request):
    var = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        experience = request.POST.get('experience', '')
        interest = request.POST.get('interest', '')
        customfile = request.FILES['customfile']
        
        # fs = FileSystemStorage()
        # fs.save(customfile.name, customfile)
        
        resume = Resume(name=name, email=email, phone=phone, experience=experience, interest=interest, resume=customfile)
        resume.save()
        file = str(customfile.name).replace(" ", "_")
        print(file)
        val = check.skills_check('media/resume/pdfs/'+ file)
        # print(interest)
        # print(val)
        
        for i in val:
            if i == interest:
                var = True
                break 
        
        if var:
            selectedCandidate = selectedResume(candidate_name=name, candidate_email=email, candidate_phone=phone, candidate_experience=experience, candidate_interest=interest, candidate_resume=customfile)
            selectedCandidate.save()
            messages.success(request, 'Your profile matches to the job requirements and has been forwarded to HR team.')
        
        else:
            messages.error(request, 'Your profile does not match with your interest.')
        # print(var)
    return render(request, 'resume/index.html')

def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'resume/contact.html', {'thank': thank})

def about(request):
    return render(request, 'resume/about.html')