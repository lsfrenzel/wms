from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from routes import movements_bp
from models import db, Product, Movement
from datetime import datetime, timedelta

@movements_bp.route('/')
@login_required
def index():
    movements = Movement.query.order_by(Movement.created_at.desc()).limit(100).all()
    products = Product.query.order_by(Product.name).all()
    
    today = datetime.now().date()
    entries_today = Movement.query.filter(
        Movement.type == 'entrada',
        db.func.date(Movement.created_at) == today
    ).count()
    
    exits_today = Movement.query.filter(
        Movement.type == 'saida',
        db.func.date(Movement.created_at) == today
    ).count()
    
    adjustments_today = Movement.query.filter(
        Movement.type == 'ajuste',
        db.func.date(Movement.created_at) == today
    ).count()
    
    stats = {
        'entries_today': entries_today,
        'exits_today': exits_today,
        'adjustments_today': adjustments_today,
        'total_movements': Movement.query.count()
    }
    
    return render_template('movements.html', movements=movements, products=products, stats=stats)

@movements_bp.route('/add', methods=['POST'])
@login_required
def add_movement():
    try:
        product_id = int(request.form.get('product_id'))
        movement_type = request.form.get('type')
        quantity = int(request.form.get('quantity'))
        notes = request.form.get('notes', '')
        
        product = Product.query.get_or_404(product_id)
        
        if movement_type == 'entrada':
            product.quantity += quantity
        elif movement_type == 'saida':
            if product.quantity < quantity:
                flash('Quantidade insuficiente em estoque!', 'danger')
                return redirect(url_for('movements.index'))
            product.quantity -= quantity
        elif movement_type == 'ajuste':
            product.quantity = quantity
        
        movement = Movement(
            product_id=product_id,
            type=movement_type,
            quantity=quantity,
            user_id=current_user.id,
            notes=notes
        )
        
        db.session.add(movement)
        db.session.commit()
        
        flash(f'Movimentação registrada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao registrar movimentação: {str(e)}', 'danger')
    
    return redirect(url_for('movements.index'))

@movements_bp.route('/delete/<int:movement_id>', methods=['POST'])
@login_required
def delete_movement(movement_id):
    try:
        movement = Movement.query.get_or_404(movement_id)
        product = movement.product
        
        if movement.type == 'entrada':
            product.quantity -= movement.quantity
        elif movement.type == 'saida':
            product.quantity += movement.quantity
        
        db.session.delete(movement)
        db.session.commit()
        
        flash('Movimentação excluída com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir movimentação: {str(e)}', 'danger')
    
    return redirect(url_for('movements.index'))
