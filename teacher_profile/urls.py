from django.urls import path
from teacher_profile import views

urlpatterns = [
    path('profiles/', views.ProfilesView.as_view(), name='profiles'),
    path('profile_details/<int:pid>/', views.ProfileDetailsView.as_view(), name='profile_details'),
    path('importer/', views.ImporterView.as_view(), name='importer'),
]
