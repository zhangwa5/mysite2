#####重用的登录和注册APP(注册功能、邮箱验证功能还未完成）  

#####简单的使用方法:  

1、创建虚拟环境   
2、使用pip安装第三方依赖:pip install -r requirements.txt  
3、修改settings.back.py文件为settings.py  
4、运行migrate命令，创建数据库和数据表  
5、要实现邮箱验证，必须在settings.py配置发生邮件参数 
```python
# settings.py 修改
# 邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'xxxxxxx@qq.com'
EMAIL_HOST_PASSWORD = 'xxxxxxx'   #此处密码非QQ邮箱密码，是在QQ邮箱设置中设置的第三方登录邮箱的授权码
# 注册有效期天数
CONFIRM_DAYS = 7
```
6、运行python manage.py runserver启动服务器  

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


