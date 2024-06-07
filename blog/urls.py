from django.urls import path

from .views import home_page, timeline_page, profile_page, handle_follow

urlpatterns = [
    path('', home_page, name='home_page'),
    path('timeline/', timeline_page, name='timeline_page'),
    path('profile/<int:user_id>/', profile_page, name='profile_page'),
    path('handle_follow/<int:user_id>/', handle_follow, name='handle_follow'),
]