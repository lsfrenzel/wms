from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from routes import shipping_bp
from models import db, Product, Shipment, ShipmentItem
from datetime import datetime

@shipping_bp.route('/')
@login_required
def index():
    shipments = Shipment.query.order_by(Shipment.created_at.desc()).all()
    
    pending = Shipment.query.filter_by(status='pending').count()
    in_progress = Shipment.query.filter_by(status='in_progress').count()
    shipped = Shipment.query.filter_by(status='shipped').count()
    
    stats = {
        'pending': pending,
        'in_progress': in_progress,
        'shipped': shipped,
        'total': Shipment.query.count()
    }
    
    return render_template('shipping.html', shipments=shipments, stats=stats)

@shipping_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_shipment():
    if request.method == 'POST':
        try:
            order_number = request.form.get('order_number')
            customer_name = request.form.get('customer_name')
            customer_address = request.form.get('customer_address')
            notes = request.form.get('notes', '')
            
            if Shipment.query.filter_by(order_number=order_number).first():
                flash('Número do pedido já existe.', 'danger')
                return redirect(url_for('shipping.add_shipment'))
            
            shipment = Shipment(
                order_number=order_number,
                customer_name=customer_name,
                customer_address=customer_address,
                status='pending',
                user_id=current_user.id,
                notes=notes
            )
            
            db.session.add(shipment)
            db.session.commit()
            
            flash(f'Expedição {order_number} criada com sucesso!', 'success')
            return redirect(url_for('shipping.view_shipment', shipment_id=shipment.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar expedição: {str(e)}', 'danger')
    
    return render_template('add_shipment.html')

@shipping_bp.route('/view/<int:shipment_id>')
@login_required
def view_shipment(shipment_id):
    shipment = Shipment.query.get_or_404(shipment_id)
    products = Product.query.filter(Product.quantity > 0).order_by(Product.name).all()
    return render_template('view_shipment.html', shipment=shipment, products=products)

@shipping_bp.route('/add_item/<int:shipment_id>', methods=['POST'])
@login_required
def add_item(shipment_id):
    try:
        shipment = Shipment.query.get_or_404(shipment_id)
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity'))
        
        product = Product.query.get_or_404(product_id)
        
        if product.quantity < quantity:
            flash('Quantidade insuficiente em estoque!', 'danger')
            return redirect(url_for('shipping.view_shipment', shipment_id=shipment_id))
        
        item = ShipmentItem(
            shipment_id=shipment_id,
            product_id=product_id,
            quantity=quantity
        )
        
        db.session.add(item)
        db.session.commit()
        
        flash(f'Item adicionado à expedição!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao adicionar item: {str(e)}', 'danger')
    
    return redirect(url_for('shipping.view_shipment', shipment_id=shipment_id))

@shipping_bp.route('/remove_item/<int:item_id>', methods=['POST'])
@login_required
def remove_item(item_id):
    try:
        item = ShipmentItem.query.get_or_404(item_id)
        shipment_id = item.shipment_id
        
        db.session.delete(item)
        db.session.commit()
        
        flash('Item removido da expedição!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao remover item: {str(e)}', 'danger')
    
    return redirect(url_for('shipping.view_shipment', shipment_id=shipment_id))

@shipping_bp.route('/update_status/<int:shipment_id>', methods=['POST'])
@login_required
def update_status(shipment_id):
    try:
        shipment = Shipment.query.get_or_404(shipment_id)
        new_status = request.form.get('status')
        
        if new_status == 'shipped' and not shipment.shipped_at:
            product_totals = {}
            for item in shipment.items:
                if item.product_id not in product_totals:
                    product_totals[item.product_id] = {
                        'product': item.product,
                        'quantity': 0
                    }
                product_totals[item.product_id]['quantity'] += item.quantity
            
            for product_id, data in product_totals.items():
                product = data['product']
                required_qty = data['quantity']
                if product.quantity < required_qty:
                    flash(f'Estoque insuficiente para {product.name}! Disponível: {product.quantity}, Necessário: {required_qty}', 'danger')
                    return redirect(url_for('shipping.index'))
            
            shipment.status = new_status
            shipment.shipped_at = datetime.utcnow()
            
            for product_id, data in product_totals.items():
                product = data['product']
                product.quantity -= data['quantity']
        else:
            shipment.status = new_status
        
        db.session.commit()
        
        flash(f'Status da expedição atualizado!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao atualizar status: {str(e)}', 'danger')
    
    return redirect(url_for('shipping.index'))

@shipping_bp.route('/delete/<int:shipment_id>', methods=['POST'])
@login_required
def delete_shipment(shipment_id):
    try:
        shipment = Shipment.query.get_or_404(shipment_id)
        order_number = shipment.order_number
        
        db.session.delete(shipment)
        db.session.commit()
        
        flash(f'Expedição {order_number} excluída com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir expedição: {str(e)}', 'danger')
    
    return redirect(url_for('shipping.index'))
