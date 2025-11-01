from flask import render_template, jsonify, Response
from flask_login import login_required
from routes import reports_bp
from models import User
from datetime import datetime, timedelta
import random
import csv
from io import StringIO

@reports_bp.route('/')
@login_required
def index():
    return render_template('reports.html')

@reports_bp.route('/api/user_stats')
@login_required
def user_stats():
    total_users = User.query.count()
    active_users = User.query.filter(User.active.is_(True)).count()
    inactive_users = total_users - active_users
    admin_users = User.query.filter_by(role='admin').count()
    regular_users = User.query.filter_by(role='user').count()
    
    return jsonify({
        'total': total_users,
        'active': active_users,
        'inactive': inactive_users,
        'admins': admin_users,
        'regular': regular_users
    })

@reports_bp.route('/api/stock_movements')
@login_required
def stock_movements():
    days = 7
    labels = []
    entries = []
    exits = []
    
    for i in range(days):
        date = datetime.now() - timedelta(days=days-i-1)
        labels.append(date.strftime('%d/%m'))
        entries.append(random.randint(10, 50))
        exits.append(random.randint(5, 45))
    
    return jsonify({
        'labels': labels,
        'entries': entries,
        'exits': exits
    })

@reports_bp.route('/api/stock_by_category')
@login_required
def stock_by_category():
    categories = ['Eletrônicos', 'Roupas', 'Alimentos', 'Móveis', 'Ferramentas', 'Outros']
    quantities = [random.randint(20, 100) for _ in range(len(categories))]
    
    return jsonify({
        'labels': categories,
        'data': quantities
    })

@reports_bp.route('/api/recent_activities')
@login_required
def recent_activities():
    activities = [
        {'type': 'Entrada', 'item': 'Notebook Dell XPS 15', 'quantity': 10, 'date': '2024-11-01 10:30'},
        {'type': 'Saída', 'item': 'Mouse Logitech MX Master', 'quantity': 5, 'date': '2024-11-01 09:15'},
        {'type': 'Entrada', 'item': 'Teclado Mecânico RGB', 'quantity': 15, 'date': '2024-10-31 16:45'},
        {'type': 'Saída', 'item': 'Monitor LG 27"', 'quantity': 3, 'date': '2024-10-31 14:20'},
        {'type': 'Entrada', 'item': 'Webcam Logitech C920', 'quantity': 8, 'date': '2024-10-31 11:00'},
        {'type': 'Ajuste', 'item': 'Headset HyperX Cloud', 'quantity': -2, 'date': '2024-10-30 15:30'},
    ]
    
    return jsonify(activities)

@reports_bp.route('/export/csv')
@login_required
def export_csv():
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Relatório de Atividades - WMS Sistema'])
    writer.writerow(['Gerado em:', datetime.now().strftime('%d/%m/%Y %H:%M')])
    writer.writerow([])
    
    writer.writerow(['Estatísticas de Usuários'])
    writer.writerow(['Tipo', 'Quantidade'])
    writer.writerow(['Total de Usuários', User.query.count()])
    writer.writerow(['Usuários Ativos', User.query.filter_by(active=True).count()])
    writer.writerow(['Administradores', User.query.filter_by(role='admin').count()])
    writer.writerow([])
    
    writer.writerow(['Atividades Recentes'])
    writer.writerow(['Tipo', 'Item', 'Quantidade', 'Data/Hora'])
    
    activities = [
        ['Entrada', 'Notebook Dell XPS 15', 10, '2024-11-01 10:30'],
        ['Saída', 'Mouse Logitech MX Master', 5, '2024-11-01 09:15'],
        ['Entrada', 'Teclado Mecânico RGB', 15, '2024-10-31 16:45'],
        ['Saída', 'Monitor LG 27"', 3, '2024-10-31 14:20'],
        ['Entrada', 'Webcam Logitech C920', 8, '2024-10-31 11:00'],
        ['Ajuste', 'Headset HyperX Cloud', -2, '2024-10-30 15:30'],
    ]
    
    for activity in activities:
        writer.writerow(activity)
    
    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename=relatorio_wms_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    return response
