from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    # path('list/', views.UserListView.as_view(), name='list'),
    # path('add/', views.UserCUView.as_view(), name='create'),
    # path('update/<int:pk>/', views.UserCUView.as_view(), name='update'),
    
    # path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # password change
    path('password_change/', views.LogoutView.as_view(), name='password_change'),
    path('password_change_done/', views.LogoutView.as_view(), name='password_change_done'),
    # password reset
    path('reset_password/', views.PasswordResetView.as_view(), name='reset_password'),
    path('password_reset_done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]