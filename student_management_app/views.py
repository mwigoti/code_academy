from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

from django.contrib import messages
from django.contrib.auth import  login, logout

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from datetime import timedelta

from student_management_app.EmailBackEnd import EmailBackEnd

from student_management_system import settings

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

from .forms import PasswordResetForm

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import SetPasswordForm



def ShowLoginPage(request):
    return render(request,"login_page.html")

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
    #    captcha_token=request.POST.get("g-recaptcha-response")
    #    cap_url="https://www.google.com/recaptcha/api/siteverify"
    #    cap_secret="6LeWtqUZAAAAANlv3se4uw5WAg-p0X61CJjHPxKT"
    #    cap_data={"secret":cap_secret,"response":captcha_token}
    #    cap_server_response=requests.post(url=cap_url,data=cap_data)
    #    cap_json=json.loads(cap_server_response.text)
#
    #    if cap_json['success']==False:
    #        messages.error(request,"Invalid Captcha Try Again")
    #        return HttpResponseRedirect("/")
#
        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type=="2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "YOUR_API_KEY",' \
         '        authDomain: "FIREBASE_AUTH_URL",' \
         '        databaseURL: "FIREBASE_DATABASE_URL",' \
         '        projectId: "FIREBASE_PROJECT_ID",' \
         '        storageBucket: "FIREBASE_STORAGE_BUCKET_URL",' \
         '        messagingSenderId: "FIREBASE_SENDER_ID",' \
         '        appId: "FIREBASE_APP_ID",' \
         '        measurementId: "FIREBASE_MEASUREMENT_ID"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")

def Testurl(request):
    return HttpResponse("Ok")

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            UserModel = get_user_model()
            user = UserModel.objects.filter(email=email).first()
            if user:
                user.password_reset_timestamp = timezone.now()
                user.save()
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                expiration_date = timezone.now() + timedelta(hours=1)  # Set expiration time to 1 hour
                reset_link = request.build_absolute_uri(reverse('password_reset_confirm', args=[uid, token, int(expiration_date.timestamp())]))
                subject = 'Password Reset Request'
                message = f'Hello {user.username},\n\nClick the following link to reset your password:\n{reset_link}\n\nThis link will expire in 30 minutes.'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [user.email]
                send_mail(subject, message, from_email, recipient_list)
                return redirect('password_reset_done')
    else:
        form = PasswordResetForm()

    return render(request, 'registration/password_reset_form.html', {'form': form})



class PasswordResetConfirmView(FormView):
    template_name = 'registration/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('password_reset_complete')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.user = self.get_user()
        kwargs['user'] = self.user
        return kwargs

    def get_user(self):
        uidb64 = self.kwargs['uidb64']
        token = self.kwargs['token']
        UserModel = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(pk=uid)
        except (UserModel.DoesNotExist, ValueError, TypeError):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            # Check if the token is still valid (e.g., not older than 1 hour)
            if user.password_reset_timestamp and (timezone.now() - user.password_reset_timestamp).total_seconds() <= 3600:
                return user
        return None

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)