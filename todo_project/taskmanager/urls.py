from django.urls import path, include
from .views import *
urlpatterns = [
    path('home/', homePage, name="home"),
    path('', loginPage, name="login"),
    path('signup/', signupPage, name="signup"),
    path('logout/', logoutPage, name="logout"),
    path('changepass/', changepassPage, name="changepass"),

    path('tasklist/', taskPage, name="task"),
    path('addtask/', addtaskPage, name="addtask"),

    path('edittask/<int:id>/', edittaskPage, name="edittask"),
    path('deletetask/<int:id>/', deletetaskPage, name="deletetask"),
    path('viewtask/<int:id>/', viewPage, name="view"),
    path('statusChange/<int:id>/', statusChange, name="status"),


]