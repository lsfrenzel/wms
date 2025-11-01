import os
from flask import Flask
from flask_login import LoginManager
from models import db, User
from routes import auth_bp, admin_bp, reports_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(reports_bp)

def init_database():
    with app.app_context():
        db.create_all()
        
        if User.query.count() == 0:
            print("Criando usuário administrador padrão...")
            admin = User(
                username='admin',
                email='admin@wms.com',
                name='Administrador',
                role='admin'
            )
            admin.set_password('admin123')
            
            user = User(
                username='user',
                email='user@wms.com',
                name='Usuário Teste',
                role='user'
            )
            user.set_password('user123')
            
            db.session.add(admin)
            db.session.add(user)
            db.session.commit()
            print("Usuários criados com sucesso!")
            print("Admin - Usuário: admin, Senha: admin123")
            print("User - Usuário: user, Senha: user123")

if __name__ == '__main__':
    init_database()
    app.run(host='0.0.0.0', port=5000, debug=True)
