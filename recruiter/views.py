from django.shortcuts import render
from django.http import HttpResponse
from .models import selectedResume
from math import ceil
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import redirect

from resume.models import Contact

def index(request):

    allCandidate = []
    intCandidate = selectedResume.objects.values('candidate_interest', 'candidate_id')
    interested = {item['candidate_interest'] for item in intCandidate}
    for interest in interested:
        candidate = selectedResume.objects.filter(candidate_interest=interest)
        n = len(candidate)
        nSlides = n // 4 + ceil((n/4) - (n//4))
        allCandidate.append([candidate, range(1, nSlides), nSlides])
    params = {'allCandidate': allCandidate}
    # print(allCandidate)
    return render(request, 'recruiter/index.html', params)

def success(request, id):

    candidate = selectedResume.objects.filter(candidate_id=id)
    candidateDetail = candidate.values('candidate_email', 'candidate_name')
    email = [item['candidate_email'] for item in candidateDetail]
    name = [item['candidate_name'] for item in candidateDetail]

    subject = 'Regarding selection for job interview'
    template = render_to_string('recruiter/email_template.html', {'candidateName': name[0]})

    email = EmailMessage(subject,
    template,
    settings.EMAIL_HOST_USER,
    [email[0]],
    )

    email.fail_silently = False
    email.send()
    candidate.delete()
    response = redirect('/recruiter/')
    return response

def decline(request, id):

    candidate = selectedResume.objects.filter(candidate_id=id)
    candidate.delete()
    response = redirect('/recruiter/')
    return response

def contact(request):

    contacts = Contact.objects.all()    
    # print(contacts)
   
    return render(request, 'recruiter/contact.html', {'contacts': contacts})  

def response(request, id):
    
    if request.method == "POST":
        reply = request.POST.get('reply', '')
    
        candidate = Contact.objects.filter(msg_id=id)
        candidateDetail = candidate.values('email', 'name')
        email = [item['email'] for item in candidateDetail]
        name = [item['name'] for item in candidateDetail]

        subject = 'Regarding your issue'
        template = render_to_string('recruiter/response_template.html', {'candidateName': name[0], 'reply': reply})
        email = EmailMessage(subject,
        template,
        settings.EMAIL_HOST_USER,
        [email[0]],
        )
        email.fail_silently = False
        email.send()

        candidate.delete()
        response = redirect('/recruiter/contact/')
    
    return response
    