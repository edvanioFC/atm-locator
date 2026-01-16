from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import ATM, User
from app.schemas import ATMCreate
from app import db
from pydantic import ValidationError
from app.utils import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# 1. Proteção Global do Blueprint
@admin_bp.before_request
@login_required
@admin_required
def check_admin():
    if current_user.username != 'admin':
        return "Acesso Negado: Apenas administradores podem aceder a esta área.", 403

@admin_bp.route('/dashboard')
def dashboard():
    atms_count = ATM.query.count()
    users_count = User.query.count()
    atms = ATM.query.all()
    return render_template(
                'admin_dashboard.html', 
                atms=atms, 
                atms_count=atms_count, 
                users_count=users_count
            )

@admin_bp.route('/atm/add', methods=['POST'])
def add_atm():
    try:
        form_data = request.form.to_dict()

        # Conversão manual para garantir tipos antes do Pydantic
        payload = {
            "bank_name": form_data.get('bank_name'),
            "address": form_data.get('address'),
            "latitude": float(form_data.get('latitude', 0)),
            "longitude": float(form_data.get('longitude', 0)),
            "is_active": form_data.get('is_active') in ('on', 'true', '1')
        }

        # Validar
        data = ATMCreate(**payload)

        #Validar se o ATM já existe na mesma localização
        existing_atm = ATM.query.filter_by(
            latitude=data.latitude, 
            longitude=data.longitude
        ).first()
        if existing_atm:
            flash('Erro: Já existe um ATM nesta localização.', 'danger')
            return redirect(url_for('admin.dashboard'))

        # Inserir
        new_atm = ATM(**data.model_dump())
        
        db.session.add(new_atm)
        db.session.commit()
        flash('ATM inserido com sucesso!', 'success')
        
    except (ValidationError, ValueError) as e:
        flash('Erro nos dados: Verifique os campos preenchidos.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro interno: {str(e)}', 'danger')
    
    return redirect(url_for('admin.dashboard'))