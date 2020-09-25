"""app_config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

# URL�̑S�̐݌v
urlpatterns = [
    # �A�v���ualatool�v�ɃA�N�Z�X����URL
    path('alatool/', include('alatool.urls')),
    # ����URL���w�肵�Ȃ��ꍇ�iapp_config/views.py�ŁA�����I�Ɂualatool�v�ɃA�N�Z�X����悤�ݒ�ς݁j
    path('', views.index, name='index'),
    # �Ǘ��T�C�g�ɃA�N�Z�X����URL
    path('admin/', admin.site.urls),
    #���O�C���@�\�ǉ��e�X�g�p
    path('', include('accounts.urls')),  #�ǉ�
]

# ���f�B�A�t�@�C�����J�p��URL�ݒ�
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)