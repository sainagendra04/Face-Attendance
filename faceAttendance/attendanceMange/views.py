from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, request, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from attendanceMange.models import *
import hashlib
import os
import cv2, json
import face_recognition
from django.contrib import auth, messages
from django.core.files.storage import FileSystemStorage
import numpy as np
from datetime import datetime,date
from django.db import connection
from django.core import serializers

# Create your views here.
def video_feed(request):
    if request.method=='GET':
        return render(request,'video_feed.html')
#@login_required(login_url='log_in')
def face_recognizer(request):
    path = 'media'
    images =[]
    names = []
    list_imgs = os.listdir(path)
    for img in list_imgs:
        cunt_img = cv2.imread(f'{path}/{img}')
        images.append(cunt_img)
        names.append(os.path.splitext(img)[0])

    encodings=[]
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodings.append(encode)

    face_encode_known = encodings

    captre = cv2.VideoCapture(0)

    while True:
        success,img = captre.read()
        #img_small = cv2.resize(img,(0,0),None,0.25,0.25)
        #img_small = cv2.cvtColor(img_small,cv2.COLOR_BGR2RGB)

        face_on_crntfrm = face_recognition.face_locations(img)
        encode_on_crntfrm = face_recognition.face_encodings(img,face_on_crntfrm)

        for encode_face,face_location in zip(encode_on_crntfrm,face_on_crntfrm):
            matching = face_recognition.compare_faces(face_encode_known,encode_face)
            face_distance = face_recognition.face_distance(face_encode_known,encode_face)

            match_index = np.argmin(face_distance)

            if matching[match_index]:
                name = names[match_index]
                y1,x2,y2,x1 = face_location
                #y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,254,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)
                # make attedance for the people here
                user = User.objects.get(pk=name)
                persn = person.objects.get(user=user.id)
                if student.objects.filter(person=persn.id).exists():
                    student_id = student.objects.get(person=persn.id)
                    # mark the attendance if the record is not found in table.
                    if studentAttend.objects.filter(student=student_id.id).exists() is not True:
                        studentAttend(student=student_id,isPresent=True,date=datetime.today(),stdattdate=datetime.today()).save()
                    else:
                        stu_attend = studentAttend.objects.filter(student=student_id.id).order_by('-id')[0]
                        if stu_attend.date.date() != date.today():
                            stu_attend = studentAttend(student=student_id,isPresent=True,date=datetime.today(),stdattdate=datetime.today()).save()
                else:
                    staff_id = staff.objects.get(person=persn.id)
                    if staffAttend.objects.filter(staff=staff_id.id,date=datetime.today()).exists() is not True:
                        staffAttend(staff=staff_id,isPresent=True,date=datetime.today(),stfattdate=datetime.today()).save()
                    else:
                        staff_attend = staffAttend.objects.filter(staff=staff_id.id).order_by('-id')[0]
                        if staff_attend.date.date() != date.today():
                            staff_attend = staffAttend(staff=staff_id,isPresent=True,date=datetime.today(),stfattdate=datetime.today()).save()
        cv2.imshow('Attendance',img)  
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    return render(request,'log_in.html')
    
@login_required(login_url='log_in')
def studentdetails(request):
    username=request.COOKIES.get('logged')
    if username:
        user = User.objects.get(id=username)
        person = peopleDetails.objects.get(id=user.id)
        context = {'address':person.city,'designation':person.Designation,'firstname':person.firstname,'lastname':person.lastname,'stream':person.Stream,'username':user.username,'hallticket':person.Rollnumber,'mobile':person.mobile,'propic':person.picture} #render(request,'details.html',{'user':username}
        return render(request,"studentdetails.html",context)
    else:
        return redirect('log_in')

def staffdetails(request):
    username=request.COOKIES.get('logged')
    if username:
        user = User.objects.get(id=username)
        person = peopleDetails.objects.get(id=user.id)
        context = {'address':person.city,'designation':person.Designation,'firstname':person.firstname,'lastname':person.lastname,'username':user.username,'mobile':person.mobile,'propic':person.picture} #render(request,'details.html',{'user':username}
        return render(request,"staffdetails.html",context)
    else:
        return redirect('log_in')

def principaldetails(request):
    username=request.COOKIES.get('logged')
    if username:
        user = User.objects.get(id=username)
        person = peopleDetails.objects.get(id=user.id)
        context = {'address':person.city,'designation':person.Designation,'firstname':person.firstname,'lastname':person.lastname,'username':user.username,'mobile':person.mobile,'propic':person.picture} #render(request,'details.html',{'user':username}
        return render(request,"principaldetails.html",context)
    else:
        return redirect('log_in')

def student_register(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        username = request.POST.get("username")
        rollnumber = request.POST.get("rollnumber")
        stream = request.POST.get("branch")
        mobile = request.POST.get("mobile")
        addressLine1 = request.POST.get("addressLine1")
        addressLine2 = request.POST.get("addressLine2")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        pass1 = request.POST.get("password")
        image = request.FILES.get("picture")        
        academicyear = request.POST.get("academicyear")
        
        passencode = hashlib.sha512(pass1.encode())
        password = passencode.hexdigest()
        if User.objects.filter(username=username).exists():
            messages.info(request,'User already exist, try with new username...')
            return redirect('student_register')
        elif student.objects.filter(rollnumber=rollnumber).exists():
            messages.info(request,'Rollnumber already exists')
            return redirect('student_register')
        elif address.objects.filter(addressLine1=addressLine1).exists():
            messages.info(request,'AddressLine1 exists...')
            return redirect('student_register')
        else:
            user = User.objects.create_user(username=username,password=password)
            user.save()
            user = User.objects.get(username=username)
            addres = address(addressLine1=addressLine1,addressLine2=addressLine2,city=city,state=state,pincode=pincode)
            addres.save()
            addres = address.objects.get(addressLine1=addressLine1,addressLine2=addressLine2)
            fs=FileSystemStorage()
            image_name = image.name
            imgname=[]
            imgname = image_name.split('.')
            imgname[0] = str(user.id)
            img = ".".join(imgname)
            filename = fs.save(img,image)
            picture = fs.url(filename)
            
            person1 = person(firstname=firstname,lastname=lastname,mobile=mobile,picture=picture,address=addres,user=user)
            person1.save()
            '''img = cv2.cvtColor(picture,cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodings.append(encode)
            names.append(username)'''
            person1 = person.objects.get(firstname=firstname,lastname=lastname)
            branc = branch.objects.get(stream=stream)
            student1 = student(rollnumber=rollnumber,academicYear=academicyear,branch=branc,person=person1)
            student1.save()
            messages.info(request,"Profile Registered...")
            return render(request,'log_in.html')
    else:
        return render(request,'student_register.html')

def staff_registration(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        username = request.POST.get("username")
        role = request.POST.get("designation")
        mobile = request.POST.get("mobile")
        addressLine1 = request.POST.get("addressLine1")
        addressLine2 = request.POST.get("addressLine2")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        pass1 = request.POST.get("password")
        image = request.FILES.get("picture") 
        
        passencode = hashlib.sha512(pass1.encode())
        password = passencode.hexdigest()
        if User.objects.filter(username=username).exists():
            messages.info(request,'User exist')
            return redirect('staff_registration')
        elif address.objects.filter(addressLine1=addressLine1).exists():
            messages.info(request,'AddressLine1 exists...')
            return redirect('staff_registration')
        else:
            user = User.objects.create_user(username=username,password=password)
            user.save()
            user = User.objects.get(username=username)
            addres = address(addressLine1=addressLine1,addressLine2=addressLine2,city=city,state=state,pincode=pincode)
            addres.save()
            addres = address.objects.get(addressLine1=addressLine1,addressLine2=addressLine2)
            fs=FileSystemStorage()
            image_name = image.name
            imgname=[]
            imgname = image_name.split('.')
            imgname[0] = str(user.id)
            img = ".".join(imgname)
            filename = fs.save(img,image)
            picture = fs.url(filename)
            person1 = person(firstname=firstname,lastname=lastname,mobile=mobile,picture=picture,address = addres,user=user)
            person1.save()
            person1 = person.objects.get(firstname=firstname,lastname=lastname)
            designate = designation.objects.get(role=role)
            staffentry = staff(designation=designate,person=person1)
            staffentry.save()
            return render(request,'log_in.html')
    else:
        return render(request,'staff_registration.html')

def log_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        passwrd = request.POST.get("password")
        
        passencode = hashlib.sha512(passwrd.encode())
        password = passencode.hexdigest()
        if User.objects.filter(username=username).exists():
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                personId = peopleDetails.objects.get(id=user.id)
                if personId.IsStaff:
                    if personId.Designation == 'PRINCIPAL':
                        login(request,user)
                        response = redirect('principaldetails')
                        response.set_cookie(key="logged",value=user.id)
                        return response                    
                    else:
                        login(request,user)
                        response = redirect('staffdetails')
                        response.set_cookie(key="logged",value=user.id)
                        return response
                else:
                    login(request,user)
                    response = redirect('studentdetails')
                    response.set_cookie(key="logged",value=user.id)
                    return response
            else:
                return redirect('log_in')
        else:
            return redirect('log_in')
    else:
        return render(request,'log_in.html')

@login_required(login_url='log_in')
def logoutUser(request):
    auth.logout(request)
    messages.info(request,"Successfully logged out...")
    responce = redirect('log_in')
    responce.delete_cookie('logged')
    return responce


@login_required(login_url='log_in')
def studentattendance(request):
    username=request.COOKIES.get('logged')
    if username:
        user = User.objects.get(id=username)
        person = peopleDetails.objects.get(id=user.id)
        context = {'firstname':person.firstname,'username':user.username,'mobile':person.mobile,} #render(request,'details.html',{'user':username}
        return render(request,'studentattendance.html',context)

def staffattendance(request):
    userid=request.COOKIES.get('logged')
    if userid:
        user = User.objects.get(id=userid)
        person = peopleDetails.objects.get(id=user.id)
        context = {'firstname':person.firstname,'username':user.username,'mobile':person.mobile,} #render(request,'details.html',{'user':username}
        return render(request,'staffattendance.html',context)

def principalattendance(request):
    userid=request.COOKIES.get('logged')
    if userid:
        user = User.objects.get(id=userid)
        person = peopleDetails.objects.get(id=user.id)
        context = {'firstname':person.firstname,'username':user.username,'mobile':person.mobile,} #render(request,'details.html',{'user':username}
        return render(request,'principalattendance.html',context)

def getstudentattendance(request):
    userid = request.COOKIES.get('logged')
    startDate = request.GET.get("start")
    endDate = request.GET.get("end")
    id = request.GET.get("id")
    
    if id is not None : userid = id

    personId = person.objects.get(user_id=userid)
    if student.objects.filter(person_id=personId.id).exists():
        studentId = student.objects.get(person_id=personId.id)
        cursor = connection.cursor()
        cursor.execute('call getstudentattendance(%s,%s,%s)',(studentId.id,startDate,endDate))
        result = cursor.fetchall()
        return JsonResponse(result,safe=False) 
        cursor.close()

def getstaffattendance(request):
    userid = request.COOKIES.get('logged')
    startDate = request.GET.get("start")
    endDate = request.GET.get("end")
    id = request.GET.get("id")
    
    if id is not None : userid = id
  
    personId = person.objects.get(user_id=userid)
    if staff.objects.filter(person_id=personId.id).exists():
        staffId = staff.objects.get(person_id=personId.id)
        cursor = connection.cursor()
        cursor.execute('call getstaffattendance(%s,%s,%s)',(staffId.id,startDate,endDate))
        result = cursor.fetchall()
        return JsonResponse(result,safe=False) 
        cursor.close()
def getstudentsbybranch(request):
    branchId = request.GET.get("id")
    cursor = connection.cursor()
    cursor.execute('call getstudentsbybranchid(%s)',(branchId))
    result = cursor.fetchall()
    return JsonResponse(result,safe=False) 
    cursor.close()

def getmystaff(request):
    getstaff = getallstaff.objects.values('id','staffname') 
    return JsonResponse(list(getstaff),safe=False)   

def manualstudentmarking(request):
    if request.method == 'POST':
        rollnumber = request.POST.get('hallticket')
        if student.objects.filter(rollnumber=rollnumber).exists():
            std_id = student.objects.get(rollnumber=rollnumber)
            if studentAttend.objects.filter(student=std_id,stdattdate=datetime.today()).exists():
                messages.error(request,"Attendance record already existed....")
                return render(request,'manualstudentmarking.html')
            else:
                studentAttend(student=std_id,isPresent=True,date=datetime.today(),stdattdate=datetime.today()).save()
                return staffattendance(request)
        else:
            messages.error(request,'Candidate not found.....')
            return render(request,'manualstudentmarking.html')
    return render(request,'manualstudentmarking.html')

def manualstaffmarking(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        if peopleDetails.objects.filter(mobile=mobile,IsStaff=True).exists():
            personId = peopleDetails.objects.get(mobile=mobile)
            if staffAttend.objects.filter(staff_id=personId.id,stfattdate=datetime.today()).exists():
                messages.error(request,"Attendance record already existed....")
                return render(request,'manualstaffmarking.html')
            else:
                staffAttend(staff_id=personId.id,isPresent=True,date=datetime.today(),stfattdate=datetime.today()).save()
                return principalattendance(request)
        else:
            messages.error(request,'Candidate not found.....')
            return render(request,'manualstaffmarking.html')
    return render(request,'manualstaffmarking.html')