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

# URLの全体設計
urlpatterns = [
    # アプリ「alatool」にアクセスするURL
    path('alatool/', include('alatool.urls')),
    # 何もURLを指定しない場合（app_config/views.pyで、自動的に「alatool」にアクセスするよう設定済み）
    path('', views.index, name='index'),
    # 管理サイトにアクセスするURL
    path('admin/', admin.site.urls),
    #ログイン機能追加テスト用
    path('', include('accounts.urls')),  #追加
]

# メディアファイル公開用のURL設定
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)