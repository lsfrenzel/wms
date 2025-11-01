from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

from routes import auth, admin, reports
