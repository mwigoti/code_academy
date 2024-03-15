from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def showDemoPage(request):
    return render(request, 'index.html')

def ShowLoginPage(request):
    return render(request, 'login.html')

def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2> Method Not Allowed </h2>")
    else:
        user=EmailBackEnd.authenticate(request,request.POST.get("email"), request.POST.get("password"))
        if user != None:
            return HttpResponse("email :"+request.POST.get("email")+"Password: "+request.POST.get("password"))
        else:
            return HttpResponse("Invalid Login")