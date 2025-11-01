import os
from flask import Flask
from flask_login import LoginManager
from models import db, User, Product
from routes import auth_bp, admin_bp, reports_bp, stock_bp, movements_bp, shipping_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 300,
    'pool_pre_ping': True,
}

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
app.register_blueprint(stock_bp)
app.register_blueprint(movements_bp)
app.register_blueprint(shipping_bp)

def init_database():
    with app.app_context():
        db.create_all()
        
        if User.query.count() == 0:
            print("Criando usuários padrão...")
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
        
        if Product.query.count() == 0:
            print("Criando produtos de exemplo...")
            products = [
                Product(code='PROD001', name='Notebook Dell XPS 15', category='Eletrônicos', unit='UN', quantity=25, min_quantity=5, location='A1-01'),
                Product(code='PROD002', name='Mouse Logitech MX Master', category='Eletrônicos', unit='UN', quantity=50, min_quantity=10, location='A1-02'),
                Product(code='PROD003', name='Teclado Mecânico RGB', category='Eletrônicos', unit='UN', quantity=30, min_quantity=8, location='A1-03'),
                Product(code='PROD004', name='Monitor LG 27"', category='Eletrônicos', unit='UN', quantity=15, min_quantity=5, location='A2-01'),
                Product(code='PROD005', name='Webcam Logitech C920', category='Eletrônicos', unit='UN', quantity=20, min_quantity=5, location='A2-02'),
            ]
            for product in products:
                db.session.add(product)
            db.session.commit()
            print("Produtos criados com sucesso!")

if __name__ == '__main__':
    init_database()
    app.run(host='0.0.0.0', port=5000, debug=True)
