from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
reports_bp = Blueprint('reports', __name__, url_prefix='/reports')
stock_bp = Blueprint('stock', __name__, url_prefix='/stock')
movements_bp = Blueprint('movements', __name__, url_prefix='/movements')
shipping_bp = Blueprint('shipping', __name__, url_prefix='/shipping')

from routes import auth, admin, reports, stock, movements, shipping
