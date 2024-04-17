from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns=[       
        path('', views.CareGiverAppointmentView.as_view(), name='index'),
        path('lab-appointments/', views.LabAppointmentView.as_view(), name='lab_appointments'),
        path('appointment/<str:uuid>/payment-status/', views.UpdatePaymentStatus.as_view(), name="payment_status"),

        # git-pull
        path('git-pull', views.GitPullView.as_view(), name='git-pull'),

        # audit-trail
        # path('audits', views.AuditTrailListView.as_view(), name='audittrail-list'),
        
        # accounts
        path('accounts/signup/', views.SignupView.as_view(), name='signup'),
        path('accounts/login/', views.LoginPageView.as_view(), name='login'),
        path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
        path('accounts/change-password/', views.ChangePasswordView.as_view(), name='change-password'),

        #grouprequiredmixin test
        path('groups/', views.GroupRequiredTestView.as_view(), name='groups-list'),


        # user crud
        path('users/', views.UserListView.as_view(), name='users-list'),
        path('users/create', views.UserCreateView.as_view(), name='users-create'),
        path('users/<int:pk>/update', views.UserUpdateView.as_view(), name='users-update'),
        path('users/<int:pk>/status', views.UserStatusView.as_view(), name='users-status'),
        path('users/<int:pk>/password-reset', views.UserPasswordResetView.as_view(), name='users-password-reset'),

        #caregiver
        path("user/<str:uuid>/caregiver/", views.CareGiverProfileView.as_view(), name="caregiver_profile"),

        path("caregiver/appointment/<int:pk>/", views.CGAppointmentDetailView.as_view(), name="cg_appt_detail"),
        path("lab/appointment/<int:pk>/", views.LabAppointmentDetailView.as_view(), name="lab_appt_detail"),

]