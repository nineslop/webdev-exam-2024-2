from app import app, db
from app.models import User, Role

with app.app_context():
    db.create_all()
    
    if not Role.query.filter_by(name='admin').first():
        admin_role = Role(name='admin', description='Администратор')
        db.session.add(admin_role)
    if not Role.query.filter_by(name='moderator').first():
        moderator_role = Role(name='moderator', description='Модератор')
        db.session.add(moderator_role)
    if not Role.query.filter_by(name='user').first():
        user_role = Role(name='user', description='Пользователь')
        db.session.add(user_role)
    
    if not User.query.filter_by(login='admin').first():
        admin_user = User(
            login='admin',
            first_name='Admin',
            last_name='User',
            role=admin_role
        )
        admin_user.set_password('adminpassword')
        db.session.add(admin_user)
    
    if not User.query.filter_by(login='moderator').first():
        moderator_user = User(
            login='moderator',
            first_name='Moderator',
            last_name='User',
            role=moderator_role
        )
        moderator_user.set_password('moderatorpassword')
        db.session.add(moderator_user)
    
    if not User.query.filter_by(login='user').first():
        normal_user = User(
            login='user',
            first_name='Normal',
            last_name='User',
            role=user_role
        )
        normal_user.set_password('userpassword')
        db.session.add(normal_user)
    
    db.session.commit()
