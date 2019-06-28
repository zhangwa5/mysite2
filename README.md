#####重用的登录和注册APP(注册功能、邮箱验证功能还未完成）  

#####简单的使用方法:  

1、创建虚拟环境   
2、使用pip安装第三方依赖:pip install -r requirements.txt  
3、修改settings.example.py文件为settings.py  
4、运行migrate命令，创建数据库和数据表  
5、运行python manage.py runserver启动服务器  

```python
from django.contrib import admin    
from django.urls import path, include   
from login import views  
urlpatterns = [  
    path('admin/', admin.site.urls),     
    path('index/', views.index),      
    path('login/', views.login),      
    path('register/', views.register),     
    path('logout/', views.logout),      
    path('confirm/', views.user_confirm),     
    path('captcha/', include('captcha.urls'))    
] 
```


