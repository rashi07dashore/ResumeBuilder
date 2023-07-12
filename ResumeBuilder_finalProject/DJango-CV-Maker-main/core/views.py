from fileinput import filename
from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import render, redirect,reverse
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout
from django.template import context
from .models import Skill,Academic,Referee,Profile,User,Skill,Cv
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password
import pdfkit




def index(request):
    return render(request, 'core/index.html')


def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect('login')
    return render(request, 'core/login.html')


@login_required
def dashboard(request):
    user_id = request.user.id

    try:
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]
        print('Cv ID is',cv_id)
        print('Data type',type(cv_id))
        if isinstance(cv_id, int):
            context = {'status':'there_is_cv'}
            return render(request, 'core/dashboard.html', context)
    except Exception as e:
        context = {'status':'no_cv'}
        return render(request, 'core/dashboard.html', context)    



def createCv(request):
    user_id = request.user.id

    try:
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]

        profile_id = Profile.objects.filter(cv_id=cv_id).values_list('id', flat=True)
        profile_id = list(profile_id)
        profile_id = profile_id[0]

        if isinstance(profile_id, int):
            context = {'status':'there_is_profile'}
            return render(request, 'core/create_cv.html', context)
    except Exception as e:
        context = {'status':'no_profile'}
        return render(request, 'core/create_cv.html', context)




def saveSkill(request):
    if request.method == 'POST':
        user_id = request.user.id
        
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]


        s_name = request.POST.getlist('s_name[]')
        s_level = request.POST.getlist('s_level[]')
        
        if(len(s_name) == 1):
            a = Skill(s_name = s_name[0], s_level=s_level[0], cv_id=cv_id)
            a.save()
            return JsonResponse({'status':1})
        else:
            for x,y in zip(s_level,s_name):
                a = Skill(s_level=x, s_name=y, cv_id=cv_id)
                a.save()
            return JsonResponse({'status':1})
    return JsonResponse({'status':0})
                



def saveEducation(request):
    if request.method == 'POST':
        name = request.POST.getlist('name[]')
        year = request.POST.getlist('year[]')
        award = request.POST.getlist('award[]')


        user_id = request.user.id
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]



        if(len(name) == 1):
            a = Academic(a_institution = name[0], a_year=year[0], a_award=award[0], cv_id=cv_id)
            a.save()
            return JsonResponse({'status':1})
        else:
            for x,y,z in zip(name,year,award):
                a = Academic(a_institution=x, a_year=y, a_award=z, cv_id=cv_id)
                a.save()
            return JsonResponse({'status':1})
    return JsonResponse({'status':0})




def saveReferee(request):
    if request.method == 'POST':
        name = request.POST.getlist('name[]')
        phone = request.POST.getlist('phone[]')
        email = request.POST.getlist('email[]')

        user_id = request.user.id
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]

        if(len(name) == 1):
            a = Referee(r_name = name[0], r_email=email[0], r_phone=phone[0], cv_id=cv_id)
            a.save()
            return JsonResponse({'status':1})
        else:
            for x,y,z in zip(name,phone,email):
                a = Referee(r_name=x, r_phone=y, r_email=z, cv_id=cv_id)
                a.save()
            return JsonResponse({'status':1})
    return JsonResponse({'status':0})





def uploadProfile(request):
    fname = request.POST.get('fname')
    mname = request.POST.get('mname')
    lname = request.POST.get('lname')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    gender = request.POST.get('gender')
    bio = request.POST.get('bio')
    dob = request.POST.get('dob')
    occupation = request.POST.get('occupation')
    country = request.POST.get('country')
    region = request.POST.get('region')
    file = request.FILES.get('file')
    user_id = request.user.id

    Cv.objects.create(user_id=user_id)

    cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
    cv_id = list(cv_id)
    cv_id = cv_id[0]
    print('Cv ID is',cv_id)



    p = Profile(fname=fname, mname=mname, lname=lname, email=email, bio=bio, dob=dob, gender=gender, occupation=occupation, country=country, region=region, avator=file,phone=phone,cv_id=cv_id)
    p.save()

    return JsonResponse({'status':1})


def updateAcademic(request):
    id = request.POST.get('id')
    institution = request.POST.get('institution')
    year = request.POST.get('year')
    award = request.POST.get('award')


    Academic.objects.filter(id=id).update(a_institution=institution, a_year=year, a_award=award)

    return JsonResponse({'status':1})



def updateProfile(request):
    id = request.POST.get('id')
    fname = request.POST.get('fname')
    mname = request.POST.get('mname')
    lname = request.POST.get('lname')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    gender = request.POST.get('gender')
    bio = request.POST.get('bio')
    dob = request.POST.get('dob')
    occupation = request.POST.get('occupation')
    country = request.POST.get('country')
    region = request.POST.get('region')
    file = request.FILES.get('file')

    user_id = request.user.id
    cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
    cv_id = list(cv_id)
    cv_id = cv_id[0]

    Profile.objects.filter(cv_id=id).update(fname=fname, mname=mname, lname=lname, email=email, bio=bio, dob=dob, gender=gender, occupation=occupation, country=country, region=region, avator=file,phone=phone,cv_id=cv_id)

    return JsonResponse({'status':1})



def registerView(request):
    if request.method == 'POST':
        username = request.POST['username']
        global email
        email = request.POST['email']
        password = request.POST['password']
        password = make_password(password)

        check_user = User.objects.filter(username=username).count()
        check_email = User.objects.filter(email=email).count()

        if(check_user > 0):
            messages.error(request, 'Username is already taken')
            return redirect('reg-form')
        elif(check_email > 0):
            messages.error(request, 'Email is already taken')
            return redirect('reg-form')
        else:
            User.objects.create(username=username, email=email, password=password)
            messages.success(request, 'Account created successfully, Please Sign In')
            return redirect('reg-form')
    else:
        return render(request, 'core/register.html')        



def logoutView(request):
    logout(request)
    return redirect('index')


def viewPDF(request, id=None):

    user_profile = Profile.objects.filter(cv_id=id)
    user_skill = Skill.objects.filter(cv_id=id).values()
    user_referee = Referee.objects.filter(cv_id=id).values()
    user_education = Academic.objects.filter(cv_id=id).values()
    
    user_profile1 = Profile.objects.get(cv_id=id)
    print(user_profile1.email) 


    context = {'user_profile':user_profile,'user_skill':user_skill,'user_referee':user_referee,'user_education':user_education}
    return render(request, 'core/pdf_template.html', context)




def editCv(request):
    return render(request, 'core/edit_cv.html')


def fetchProfile(request):
    id = request.POST.get('id')
    print('Cv ID is',id)
    
    user_profile = Profile.objects.get(cv_id=id)

    
    user_profile = {'fname':user_profile.fname, 
    'mname':user_profile.mname,
    'lname':user_profile.lname,
    'email':user_profile.email,
    'phone':user_profile.phone,
    'bio':user_profile.bio,
    'dob':user_profile.dob,
    'country':user_profile.country,
    'region':user_profile.region,
    'occupation':user_profile.occupation
    }
    return JsonResponse(user_profile)



def fetchAcademic(request):
    id = request.POST.get('id')
    print('Cv ID is',id)
    
    user_education = Academic.objects.get(id=id)

    user_education = {'institution':user_education.a_institution, 
    'year':user_education.a_year,
    'award':user_education.a_award
    }
    return JsonResponse(user_education)




def deleteProfile(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print('Cv ID is',id)
        
        user_profile = Profile.objects.get(cv_id=id)
        user_profile.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})





def deleteAcademic(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print('Cv ID is',id)
        
        user_education = Academic.objects.get(id=id)
        user_education.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})



def educationView(request):
    id = request.user.cv.id
    print('Cv ID is',id)
    user_education = Academic.objects.filter(cv_id=id).all()
    context = {'user_education':user_education}
    return render(request, 'core/education_view.html', context)



def takeSS(request):  # this will generate a pdf of cv 
    import pyautogui
    from PIL import Image
    import time

# Take a screenshot of the screen
    time.sleep(2)
    screenshot = pyautogui.screenshot()

# Save the screenshot as a PNG image
    screenshot.save('screenshot.png')

# Open the image with Pillow
    img = Image.open('screenshot.png')

    left = 650
    top = 180
    right = 1250
    bottom = 1000
    box = (left, top, right, bottom)

# Crop the image
    cropped_img = img.crop(box)

# Save the cropped image
    cropped_img.save('cropped.png')




    from fpdf import FPDF

# Open the image file
    img = Image.open('cropped.png')

# Get the dimensions of the image
    img_width, img_height = img.size

# Set the dimensions of the PDF page
    pdf_width = img_width / 72 # Convert pixels to inches
    pdf_height = img_height / 72 # Convert pixels to inches

# Create a new PDF object
    pdf = FPDF(unit='in', format=(pdf_width, pdf_height))

# Add a new page to the PDF
    pdf.add_page()

# Add the image to the PDF
    pdf.image('cropped.png', 0, 0)
    
# Save the PDF file
    pdf.output('cv.pdf', 'F')
    return render(request,"core/generated.html")


def email(request,id=None):
  

#   eaddress=input("enter email address : ")
  from email.message import EmailMessage
  import ssl
  import smtplib

#   id = request.POST.get('id')
  user_profile1 = Profile.objects.get(cv_id=id)
  #u_mail=user_profile1.email

  sender='cm.cloudspace@gmail.com'  # senders email address 
  password='ywafwjvbsctavaix'      # sender's password generated by google password app 
 # reciever=u_mail  # reciever's address  
  reciever='dashore.rashi07@gmail.com'  # reciever's address 
  #print(reciever)
#   reciever='chitreshmourya3@gmail.com'
   reciever=eaddress

  subject=" Python generated email"     # subject of the email 

  body=" THIS IS YOUR CV GENERATED BY ONLINE getYourCV.com"   # body 

  em=EmailMessage()  # creating the object of EmailMessage() class 
  em['From']=sender
  em['To']=reciever
  em['Subject']=subject

  em.set_content(body)

  
  files = ["cv.pdf"] # you add send multiple pdfs using this format  , you have to just pdf file name in this list and works 
  for file in files:
    with open(file, 'rb') as f:
        file_data = f.read()
        file_name = f.name

    em.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)



  context= ssl.create_default_context()



  smtp= smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) 
  smtp.login(sender,password)    

  smtp.send_message(em)# sending the mail 




  print("\nEMAIL SENT SUCCESSFULLY ")




def generate_PDF(request, id=None):
    # print('Download Cv Id is',id)
    # pdf = pdfkit.from_url(request.build_absolute_uri(reverse('cv-detail', args=[id])), False)
    # response = HttpResponse(pdf, content_type='application/pdf') 
    # response['Content-Disposition'] = 'attachment; filename="cv.pdf"'
    # return response
    # pdfkit.from_file("pdf_template.html","cv.pdf")

    email(request,id)
    
    return render(request,'core/sent.html')
    


