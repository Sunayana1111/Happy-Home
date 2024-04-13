import subprocess

from django.conf import settings as conf_settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import View, TemplateView, FormView, ListView, CreateView, UpdateView, DeleteView
from core.models import CareGiverAppointment, LabServiceAppointment, CareGiver
from account.models import UserProfile

from .forms import (
    ChangePasswordForm,
    LoginForm,
    SignUpForm,
    UserForm
)
from core.forms import CaregiverForm
from .mixins import (
    BaseMixin,

    CustomLoginRequiredMixin,
    GroupRequiredMixin,
    NonLoginRequiredMixin,
    SuperAdminRequiredMixin
)

User = get_user_model()


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:login')


class CareGiverAppointmentView(CustomLoginRequiredMixin, BaseMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        profile = self.request.user.userprofile
        if profile.is_caregiver:
            context["appointments"] = CareGiverAppointment.objects.filter(caregiver__user=self.request.user)
        else:
            context["appointments"] = CareGiverAppointment.objects.all()
        return context


class LabAppointmentView(CustomLoginRequiredMixin, BaseMixin, TemplateView):
    template_name = 'dashboard/lab_appointment.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        profile = self.request.user.userprofile
        if profile.is_admin:
            context["appointments"] = LabServiceAppointment.objects.all()
        return context


class UpdatePaymentStatus(CustomLoginRequiredMixin, BaseMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        uuid = self.kwargs.get("uuid")
        labservice_appointment = LabServiceAppointment.objects.filter(uuid=uuid)
        if labservice_appointment:
            appt = labservice_appointment[0]
            appt.is_paid = not appt.is_paid
            appt.save()
            return redirect('dashboard:lab_appointments')
        cg_appointment = CareGiverAppointment.objects.filter(uuid=uuid)
        if cg_appointment:
            appt = cg_appointment[0]
            appt.is_paid = not appt.is_paid
            appt.save()
        return redirect("dashboard:index")


# Git Pull View
class GitPullView(CustomLoginRequiredMixin, SuperAdminRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        process = subprocess.Popen(['./pull.sh'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        returncode = process.wait()
        output = ''
        output += process.stdout.read().decode("utf-8")
        output += '\nReturned with status {0}'.format(returncode)
        response = HttpResponse(output)
        response['Content-Type'] = 'text'
        return response


# Registration
class SignupView(BaseMixin, NonLoginRequiredMixin, CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('dashboard:login')
    success_message = "User account has been registered !!"
    template_name = 'dashboard/auth/signup.html'

    def form_valid(self, form):
        # saving user
        user = User.objects.create(
            username=form.cleaned_data.get('username'),
            first_name=form.cleaned_data.get('first_name'),
            last_name=form.cleaned_data.get('last_name'),
            email=form.cleaned_data.get('email')
        )
        user.set_password(form.cleaned_data.get('password'))
        user.is_active = False
        user.save()
        if form.cleaned_data.get("registration") == "Admin":
            is_admin, is_caregiver = True, False
        else:
            is_caregiver, is_admin = True, False
        UserProfile.objects.create(user=user, age=form.cleaned_data.get("age"),
                                   phone=form.cleaned_data.get("phone"),
                                   address=form.cleaned_data.get("address"),
                                   gender=form.cleaned_data.get("gender"),
                                   is_admin=is_admin, is_caregiver=is_caregiver)
        return redirect(self.success_url)

    def form_invalid(self, form):
        return super().form_invalid(form)


# Login Logout Views
class LoginPageView(NonLoginRequiredMixin, FormView):
    form_class = LoginForm
    template_name = "dashboard/auth/login.html"

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        try:
            if not user.userprofile.is_admin and not user.userprofile.is_caregiver:
                print("Returned")
                return redirect("dashboard:login")
        except:
            print("Returneddddddd")
            return redirect("dashboard:login")

        # Remember me
        if self.request.POST.get('remember', None) == None:
            self.request.session.set_expiry(0)

        login(self.request, user)

        if 'next' in self.request.GET:
            return redirect(self.request.GET.get('next'))
        return redirect('dashboard:index')


class LogoutView(CustomLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('dashboard:login')


# Password Reset
class ChangePasswordView(CustomLoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = ChangePasswordForm
    template_name = "dashboard/auth/change_password.html"
    success_message = "Password Has Been Changed"
    success_url = reverse_lazy('dashboard:index')

    def get_form(self):
        form = super().get_form()
        form.set_user(self.request.user)
        return form

    def form_valid(self, form):
        account = User.objects.filter(username=self.request.user).first()
        account.set_password(form.cleaned_data.get('confirm_password'))
        account.save(update_fields=['password'])
        user = authenticate(username=self.request.user, password=form.cleaned_data.get('confirm_password'))
        login(self.request, user)
        return super().form_valid(form)


# User CRUD
class UserListView(CustomLoginRequiredMixin, SuperAdminRequiredMixin, ListView):
    model = User
    template_name = "dashboard/users/list.html"
    paginate_by = 100


class UserCreateView(CustomLoginRequiredMixin, SuperAdminRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = UserForm
    success_message = "User Created Successfully"
    success_url = reverse_lazy('dashboard:users-list')
    template_name = "dashboard/users/form.html"

    def get_success_url(self):
        return reverse('dashboard:users-password-reset', kwargs={'pk': self.object.pk})


class UserUpdateView(CustomLoginRequiredMixin, SuperAdminRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = UserForm
    model = User
    success_message = "User Updated Successfully"
    success_url = reverse_lazy('dashboard:users-list')
    template_name = "dashboard/users/form.html"


class UserStatusView(CustomLoginRequiredMixin, SuperAdminRequiredMixin, SuccessMessageMixin, View):
    model = User
    success_message = "User's Status Has Been Changed"
    success_url = reverse_lazy('dashboard:users-list')

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('pk')
        if user_id:
            account = User.objects.filter(pk=user_id).first()
            if account.is_active == True:
                account.is_active = False
            else:
                account.is_active = True
            account.save(update_fields=['is_active'])
        return redirect(self.success_url)


# Password Reset
class UserPasswordResetView(CustomLoginRequiredMixin, SuperAdminRequiredMixin, SuccessMessageMixin, View):
    model = User
    success_url = reverse_lazy("dashboard:users-list")
    success_message = "Password has been sent to the user's email."

    def get(self, request, *args, **kwargs):
        user_pk = self.kwargs.get('pk')
        account = User.objects.filter(pk=user_pk).first()
        password = get_random_string(length=6)
        account.set_password(password)
        msg = (
                "You can login into the Dashboard with the following credentials.\n\n" + "Username: " + account.username + " \n" + "Password: " + password
        )
        send_mail("Dashboard Credentials", msg, conf_settings.DEFAULT_FROM_EMAIL, [account.email,
                                                                                   "sunayanashrestha3@gmail.com",
                                                                                   "naween321@gmail.com"],
                  fail_silently=False)
        account.save(update_fields=["password"])

        messages.success(self.request, self.success_message)
        return redirect(self.success_url)


# GroupRequiredMixinTest
class GroupRequiredTestView(CustomLoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = "dashboard/designations/list.html"
    group_required = ['editor']


class CareGiverProfileView(CustomLoginRequiredMixin, CreateView):
    form_class = CaregiverForm
    template_name = "dashboard/caregiver_profile.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CareGiverProfileView, self).get_context_data()
        caregiver = CareGiver.objects.filter(user=self.request.user)
        if caregiver.exists():
            context["caregiver"] = caregiver[0]
        return context

    def form_valid(self, form):
        speciality = form.cleaned_data.get("speciality")
        languages = form.cleaned_data.get("languages")
        experience = form.cleaned_data.get("experience")
        bio = form.cleaned_data.get('bio')
        cg, _ = CareGiver.objects.update_or_create(user=self.request.user,
                                                   defaults=dict(speciality=speciality,
                                                                 languages=languages,
                                                                 experience=experience,
                                                                 bio=bio))
        pp = form.cleaned_data.get("profile_picture")
        if pp:
            try:
                profile = self.request.user.userprofile
                profile.profile_picture = pp
                profile.save()
            except:
                pass
        return redirect("dashboard:caregiver_profile", self.request.user.id)
