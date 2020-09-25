from django.urls import path
from . import views

app_name = 'alatool'
urlpatterns = [
    path('top/', views.top, name='top'),
    path('info/', views.info, name='info'),
    path('register/', views.register, name='register'),
    path('history/', views.history, name='history'),
    path('detail/<int:sample_id>', views.detail, name='detail'),
    path('edit/<int:sample_id>', views.edit, name='edit'),
    path('delete/<int:sample_id>', views.delete, name='delete'),
]