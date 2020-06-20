from flask import jsonify,render_template ,request,session,Blueprint,json,send_from_directory
from flask_login import login_user,logout_user,login_required,current_user
from models import User
from config import mail,msg,db,allowed_file,rd
import random,os


user=Blueprint('user',__name__,url_prefix='/api')


@user.route('/login',methods=['POST'])
def login():
    dict = json.loads(request.get_data(as_text=True))
    user_id = dict.get('login_id','')
    password = dict.get('login_password','')
    user = User.query.get(user_id)
    if user and password == user.password:
        login_user(user,remember=True)
        return jsonify({'status':'success'})
    return jsonify({'status':'fail'})


@user.route('/register',methods=['POST'])
def register():
    dict = json.loads(request.get_data(as_text=True))
    user_id = dict.get('register_email','')
    name = dict.get('register_name', '')
    password = dict.get('register_password','')
    code = dict.get('register_code', '')
    avatar = dict.get('file','/static/haimianbaobao.jpeg')
    if code != rd.get(user_id):
        return jsonify({'status': '验证码错误'})
    try:
        user = User(id=user_id,password=password,name=name,avatar=avatar)
        db.session.add(user)
        db.session.commit()
        rd.delete(user_id)
    except:
        return jsonify({'status':'该账号已被注册'})
    return jsonify({'status':'success'})


@user.route('/logout/')
@login_required
def logout():
    logout_user()
    return jsonify({'status':'success'})


@user.route('/send_email',methods=['POST'])
def send_email():
    dict=json.loads(request.get_data(as_text=True))
    email = dict.get('register_email','')
    msg.recipients=[]
    msg.recipients.append(email)
    code = ''
    for i in range(0,4):
        code += str(random.randint(0,9))
    msg.body = '您的验证码为'+code
    mail.send(msg)
    rd.set(email,code)
    return jsonify({'status':'success'})


@user.route('/upload',methods=['POST'])
def upload():
    avatar = request.files.get('file')
    if not avatar:
        icon = '/static/haimianbaobao.jpeg'
    elif not allowed_file(avatar.filename):
        return jsonify({'status': '图片格式不支持'})
    else:
        path = r'./static'
        avatar.save(os.path.join(path, avatar.filename))
        icon = '/static/' + avatar.filename
    return jsonify({'icon':icon})


@user.route('/get_user_info/')
@login_required
def getinfo():
    user = User.query.get(current_user.id)
    return jsonify({'账号':user.id,'用户名':user.name,'头像':user.avatar})


@user.route('/edit_user_info',methods=['POST'])
@login_required
def editinfo():
    user = User.query.get(current_user.id)
    dict = json.loads(request.get_data(as_text=True))
    name = dict.get('edit_name', '')
    password = dict.get('edit_password', '')
    avatar = dict.get('edit_file', '')
    if name:
        user.name=name
    if password:
        user.password=password
    if avatar:
        user.avatar=avatar
    db.session.commit()
    return jsonify({'用户名':user.name,'头像':user.avatar})


@user.route('/static/<filename>')
def getfile(filename):
    path=os.getcwd()+'/static'
    return send_from_directory(path,filename)