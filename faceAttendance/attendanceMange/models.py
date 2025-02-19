from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.
'''class users(models.Model):
    username = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=500)
    isActive = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True, auto_now_add=False)
    class Meta: db_table = "users"'''

class address(models.Model):
    addressLine1 = models.CharField(max_length=50,blank=False)
    addressLine2 = models.CharField(max_length=50,blank=False)
    city = models.CharField(max_length=30,blank=False)
    state = models.CharField(max_length=30,blank=False)
    pincode = models.IntegerField(max_length=6,blank=False)
    class Meta:
        db_table ="address"

class person(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=30,blank=False)
    lastname = models.CharField(max_length=30,blank=False)
    mobile = models.EmailField(max_length=254)
    address = models.ForeignKey(address,on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="media")
    class Meta:
        db_table = "person"

class branch(models.Model):
    stream  = models.CharField(max_length=5,blank=False)
    class Meta:
        db_table = "branch"

class designation(models.Model):
    role = models.CharField(max_length=20)
    class Meta:
        db_table = "designation"

class student(models.Model):
    person = models.ForeignKey(person, on_delete=models.CASCADE)
    rollnumber = models.CharField(max_length=10,blank=False)
    branch = models.ForeignKey(branch,on_delete=models.CASCADE)
    academicYear = models.CharField(max_length=10)
    class Meta:
        db_table = "student"

class staff(models.Model):
    person = models.ForeignKey(person,on_delete=models.CASCADE)
    designation = models.ForeignKey(designation,on_delete=models.CASCADE)
    class Meta:
        db_table = "staff"

class studentAttend(models.Model):
    student = models.ForeignKey(student,on_delete=models.CASCADE)
    isPresent = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=False, auto_now_add = True)
    stdattdate = models.DateField(auto_now=False, auto_now_add=True,blank=False)
    class Meta:
        db_table = "studentAttendance"

class staffAttend(models.Model):
    staff = models.ForeignKey(staff,on_delete=models.CASCADE)
    isPresent = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=False, auto_now_add = True)
    stfattdate = models.DateField(auto_now=False, auto_now_add=True,blank=False)
    class Meta:
        db_table = "staffAttendance"

class holidays(models.Model):
    days = models.DateField(auto_now=False, auto_now_add=False)
    class Meta:
        db_table = "holidays"
class peopleDetails(models.Model):
    id = models.BigIntegerField(primary_key=True)
    PersonId = models.BigIntegerField()
    firstname = models.CharField(max_length=30,blank=False)
    lastname = models.CharField(max_length=30,blank=False)
    mobile = models.EmailField(max_length=254)
    picture = models.ImageField()
    addressLine1 = models.CharField(max_length=50,blank=False)
    addressLine2 = models.CharField(max_length=50,blank=False)
    city = models.CharField(max_length=30,blank=False)
    IsStaff = models.BooleanField(default=False)
    Designation = models.CharField(max_length=50,blank=False)
    Stream = models.CharField(max_length=5,blank=False)
    Rollnumber = models.CharField(max_length=10,blank=False)
    class Meta:
        db_table = "peopleDetails"

class getallstaff(models.Model):
    staffname = models.CharField(max_length=100)
    class Meta:
        db_table = "getallstaff"