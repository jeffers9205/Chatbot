from django.contrib import admin
from django.urls import path
from chatbot import views  
# from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('queries/', views.queries_list, name='queries_list'),
    path('queries/add/', views.queries_add, name='queries_add'),
    path('queries/update/<int:id>/', views.queries_update, name='queries_update'),
    path('queries/delete/<int:id>/', views.queries_delete, name='queries_delete'),
    path('sendmessage/', views.send_message, name='send_message'),  
    path('chat/', views.chat_view, name='chat'),  
    path('', views.index, name='index')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)