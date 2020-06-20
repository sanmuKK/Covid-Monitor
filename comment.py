from flask import jsonify,Blueprint,request
from flask_login import login_required,current_user
from flask_socketio import emit
from models import Comment,Reply
from config import socketio,db
import json

comment=Blueprint('comment',__name__,url_prefix='/api')


@comment.route('/getcomments')
def getcomments():
    c1 = Comment.query.all()
    list = []
    for i in c1:
        replies_list=[]
        for j in i.reply:
            reply_dict={
                'reply':j.comment,
                'id':j.owner_user_reply.id,
                'name':j.owner_user_reply.name,
                'time':j.time.strftime('%Y-%m-%d %H:%M')
            }
            replies_list.append(reply_dict)
        dict={'floor':i.id,'comment':i.comment,
              'name':i.owner_user.name,
              'id':i.owner_user.id,
              'avatar':i.owner_user.avatar,
              'time':i.time.strftime('%Y-%m-%d %H:%M'),
              'replies':replies_list}
        list.append(dict)
    return jsonify(list)


@comment.route('/get_comment_user')
def get_comment_user():
    id = request.args.get('comment_id','')
    c = Comment.query.get(id)
    return jsonify({'user':c.comments_id})


@comment.route('/del_comment',methods=['DELETE'])
@login_required
def del_comment():
    dict = json.loads(request.get_data(as_text=True))
    #dict = request.form
    id = dict.get('comment_id',0)
    c = Comment.query.get(int(id))
    if c:
        if c.comments_id == current_user.id:
            db.session.delete(c)
            db.session.commit()
            return jsonify({'status':'success'})
    return jsonify({'status': 'fail'})


@socketio.on('comment')
@login_required
def comments(data):
    comments=Comment(comment=data['comment'],comments_id=current_user.id)
    db.session.add(comments)
    db.session.commit()
    emit('comment',{'comment':data['comment'],'floor':comments.id,
                    'name': comments.owner_user.name,
                    'id': comments.owner_user.id,
                    'avatar': comments.owner_user.avatar,
                    'time':comments.time.strftime('%Y-%m-%d %H:%M'),
                    'replies':[]},broadcast=True)


@socketio.on('reply')
@login_required
def reply(data):
    replies=Reply(replies_id=data['id'],comment=data['replies'],replies_id_user=current_user.id)
    db.session.add(replies)
    db.session.commit()
    list=[]
    comment_s=replies.owner_comment
    for i in comment_s.reply:
        dict={
            'reply':i.comment,
            'id': i.owner_user_reply.id,
            'name':i.owner_user_reply.name,
            'time':i.time.strftime('%Y-%m-%d %H:%M')
        }
        list.append(dict)
    emit('reply',{'comment':comment_s.comment,'floor':data['id'],
                  'name':comment_s.owner_user.name,
                  'id':comment_s.owner_user.id,
                  'avatar':comment_s.owner_user.avatar,
                  'time':comment_s.time.strftime('%Y-%m-%d %H:%M'),
                  'replies':list},broadcast=True)