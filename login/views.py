from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from . import models
from . import forms
import hashlib
import datetime
# Create your views here.
# 创建确认码对象的方法
def make_confirm_string(user):
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	code = hash_code(user.name, now)
	models.ConfirmString.objects.create(code=code, user=user)
	return code
# 发生确认邮件方法
def send_email(email, code):
	from django.core.mail import EmailMultiAlternatives
	subject = "来自金控征信官网的注册确认邮件"
	text_content = '''感谢注册金控征信官网，如果你看到此信息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
	html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.jkzx.com</a>，\
                    这里是金控征信官网！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)
	msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
	msg.attach_alternative(html_content, "text/html")
	msg.send()
def index(request):
	if not request.session.get('is_login', None):
		return redirect('/login/')
	return render(request, 'login/index.html')

def login(request):
	# 判断当前用户是否已登录，即判断session,如果是在线，则跳转到index页面
	if request.session.get('is_login', None):
		return redirect('/index/')
	if request.method == "POST":
		login_form = forms.UserForm(request.POST)
		message = "请检查填写的内容!"
		if login_form.is_valid():
			username = login_form.cleaned_data.get('username')
			password = login_form.cleaned_data.get('password')
			try:
				user = models.User.objects.get(name=username)
			except:
				message="你输入的用户不存在！"
				# 用户不存在的错误信息提示给用户
				return render(request, 'login/login.html', locals())
			# 如果用户未经过邮件确认，则不允许登录
			if  not user.has_confirmed:
				message = '该用户还未经过邮件确认！'
				return render(request, 'login/login.html', locals())
			# 如果用户验证通过后再验证密码是否正确
			if user.password == hash_code(password):
				request.session['is_login'] = True
				request.session['user.id'] = user.id
				request.session['user_name'] = user.name
				# print(username, password)
				# 用户密码正确，跳转到默认页index
				return redirect('/index/')
			else:
				message = "密码错误，请重新登录！"
				return render(request, 'login/login.html', locals())
		else:
			return render(request, 'login/login.html', locals())
	login_form = forms.UserForm()
	# 否则继续回到登录页面重新登录
	return render(request, 'login/login.html', locals())
# 注册视图
def register(request):
	if request.session.get('is_login', None):
		return redirect('/index/')
	if request.method == 'POST':
		register_form = forms.RegisterForm(request.POST)
		message = "请检查填写的内容！"
		if register_form.is_valid():
			username = register_form.cleaned_data.get('username')
			password1 = register_form.cleaned_data.get('password1')
			password2 = register_form.cleaned_data.get('password2')
			email = register_form.cleaned_data.get('email')
			sex = register_form.cleaned_data.get('sex')
			if password1 != password2:
				message = "两次输入的密码不同！"
				return render(request, 'login/register.html', locals())
			else:
				# 判断注册提交的用户名是否和表里已存在用户一样
				same_name_user = models.User.objects.filter(name=username)
				if same_name_user:
					message = "该用户已经被注册了！"
					return render(request, 'login/register.html', locals())
				same_email_user = models.User.objects.filter(email=email)
				if same_email_user:
					# 判断邮箱是否已注册
					message = '该邮箱已经被注册了！'
					return render(request, 'login/register.html', locals())
				# 当注册提交的所有信息都合法时，实例化User()类，并写入数据库表
				new_user = models.User()
				new_user.name = username
				new_user.password = hash_code(password1)
				new_user.email = email
				new_user.sex = sex
				# 保存数据至数据库
				new_user.save()
				# 生产注册码
				code = make_confirm_string(new_user)
				send_email(email, code)
				# message = "恭喜你," + username + "已注册成功！"
				# 注册成功，跳转到登录界面登录
				# return render(request, 'login/login.html', locals())
				return redirect('/login/')
		else:
			return render(request, 'login/register.html', locals())
	register_form = forms.RegisterForm()
	return render(request, 'login/register.html', locals())

# 登出视图
def logout(request):
	if not request.session.get('is_login', None):
		return redirect('/login/')
	request.session.flush()
	return redirect('/login/')

# 编写哈希加密函数加密密码
def hash_code(s, salt='hfdfsd8&*&*^^%jkfsnv&%^$#%$^&*'):
	h = hashlib.sha256()
	s += salt
	h.update(s.encode())
	return h.hexdigest()
def user_confirm(request):
	code = request.GET.get('code', None)
	message = ""
	try:
		confirm = models.ConfirmString.objects.get(code=code)
	except:
		message = "效的确认请求!"
		return render(request, 'login/confirm.html', locals())
	c_time = confirm.c_time
	now = datetime.datetime.now()
	if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
		confirm.user.delete()
		message = "您的邮件已经过期！请重新注册!"
		return render(request, 'login/confirm.html', locals())
	else:
		confirm.user.has_confirmed = True
		confirm.user.save()
		confirm.delete()
		messgae = "感谢确认，请使用账户登录！"
		return render(request, 'login/confirm.html', locals())
