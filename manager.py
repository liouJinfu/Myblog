#-*- encoding=UTF-8 -*-

from Liusblog import app, db
from flask_script import Manager
from Liusblog.models import User, Image, Comment
import random
from sqlalchemy import or_, and_
manager = Manager(app)

def getImageUrl():
    return 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'
@manager.command
def init_database():
    db.drop_all()
    ##创建表
    db.create_all()
    ##Insert 插入数据
    for i in range(0, 100):
        db.session.add(User('user'+ str(i+1), 'a' + str(i+1)))
        for j in range(0, 3):
            db.session.add(Image(getImageUrl(), str(i+1)))
            for k in range(0, 3):
                db.session.add(Comment('comments'+str(k),  1+3*i+j, i+1))
    db.session.commit()

    ###查询
    print 1, User.query.all()
    print 2, User.query.get(3)
    print 3, User.query.filter_by(id = 5).first()
    print 4, User.query.order_by(User.id.desc()).offset(1).limit(2).all()
    print 5, User.query.filter(User.username.endswith('0')).limit(3).all()
    print 6, User.query.filter(and_(User.id > 88, User.id < 99)).limit(3).all()
    print 7, User.query.order_by(User.id.desc()).paginate(page=2, per_page=10).items
    user = User.query.get(1)
    print 8, user.images.all()

    image = Image.query.get(1)
    print 9, image.user

    ##更新
    for i in range(50, 100, 1):
        user = User.query.get(i)
        user.username = '[New]' + user.username
    db.session.commit()
    User.query.filter_by(id = 1).update({'username' : '[New2]'})
    db.session.commit()

    ## 删除
    # for i in range(5, 100):
    #     comment = Comment.query.get(i)
    #     db.session.delete(comment)
    # db.session.commit()
    # Comment.query.filter(id > 50).delete()
    # db.session.commit()

if __name__ == '__main__':
    manager.run()