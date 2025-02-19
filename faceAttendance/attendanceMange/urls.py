from django.contrib import admin
from django.urls import path
from attendanceMange import views

urlpatterns = [
    path("student_register",views.student_register,name="student_register"),
    path("staff_registration",views.staff_registration,name="staff_registration"),
    path("log_in",views.log_in,name="log_in"),
    path("studentdetails",views.studentdetails,name="studentdetails"),
    path("staffdetails",views.staffdetails,name="staffdetails"),
    path("facerecognizer",views.face_recognizer,name="facerecognizer"),
    path("logout",views.logoutUser,name="logout"),
    path("studentattendance",views.studentattendance,name="studentattendance"),
    path("staffattendance",views.staffattendance,name="staffattendance"),
    path("getstudentattendance",views.getstudentattendance,name="getstudentattendance"),
    path("getstaffattendance",views.getstaffattendance,name="getstaffattendance"),
    path("getstudentsbybranch",views.getstudentsbybranch,name="getstudentsbybranch"),
    path("principaldetails",views.principaldetails,name="principaldetails"),
    path("principalattendance",views.principalattendance,name="principalattendance"),
    path("getmystaff",views.getmystaff,name="getmystaff"),
    path("manualstudentmarking",views.manualstudentmarking,name="manualstudentmarking"),
    path("manualstaffmarking",views.manualstaffmarking,name="manualstaffmarking"),

]
