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
        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"), password=request.POST.get("password"))
        if user != None:
            login(request.user)
            return HttpResponse("email :"+request.POST.get("email")+"Password: "+request.POST.get("password"))
        else:
            return HttpResponse("Invalid Login")

def GetUserDetails(request):
    if request.user != None:

        return HttpResponse("User :" +request.user.email+"user_type :"+request.user.user_type)

    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")