from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from routes import stock_bp
from models import db, Product

@stock_bp.route('/')
@login_required
def index():
    products = Product.query.order_by(Product.name).all()
    low_stock = Product.query.filter(Product.quantity <= Product.min_quantity).count()
    total_products = Product.query.count()
    total_items = db.session.query(db.func.sum(Product.quantity)).scalar() or 0
    
    stats = {
        'total_products': total_products,
        'total_items': total_items,
        'low_stock': low_stock
    }
    
    return render_template('stock.html', products=products, stats=stats)

@stock_bp.route('/add', methods=['POST'])
@login_required
def add_product():
    try:
        code = request.form.get('code')
        name = request.form.get('name')
        description = request.form.get('description', '')
        category = request.form.get('category')
        unit = request.form.get('unit', 'UN')
        quantity = int(request.form.get('quantity', 0))
        min_quantity = int(request.form.get('min_quantity', 10))
        location = request.form.get('location', '')
        
        if Product.query.filter_by(code=code).first():
            flash('Código do produto já existe.', 'danger')
            return redirect(url_for('stock.index'))
        
        product = Product(
            code=code,
            name=name,
            description=description,
            category=category,
            unit=unit,
            quantity=quantity,
            min_quantity=min_quantity,
            location=location
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash(f'Produto {name} adicionado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao adicionar produto: {str(e)}', 'danger')
    
    return redirect(url_for('stock.index'))

@stock_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        try:
            product.code = request.form.get('code')
            product.name = request.form.get('name')
            product.description = request.form.get('description', '')
            product.category = request.form.get('category')
            product.unit = request.form.get('unit', 'UN')
            product.quantity = int(request.form.get('quantity', 0))
            product.min_quantity = int(request.form.get('min_quantity', 10))
            product.location = request.form.get('location', '')
            
            db.session.commit()
            flash(f'Produto {product.name} atualizado com sucesso!', 'success')
            return redirect(url_for('stock.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar produto: {str(e)}', 'danger')
    
    return render_template('edit_product.html', product=product)

@stock_bp.route('/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        name = product.name
        db.session.delete(product)
        db.session.commit()
        
        flash(f'Produto {name} excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir produto: {str(e)}', 'danger')
    
    return redirect(url_for('stock.index'))
