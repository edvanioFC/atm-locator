from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.schemas.user_schema import UserCreate # Importando o Schema Pydantic
from app import db
from pydantic import ValidationError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        try:
            # 1. Validação rigorosa com Pydantic
            user_data = UserCreate(
                username=request.form.get('username') or '',
                email=request.form.get('email') or '',
                password=request.form.get('password') or ''
            )

            # 2. Verificar se utilizador ou email já existem
            if User.query.filter((User.username == user_data.username) | (User.email == user_data.email)).first():
                flash('Usuário ou Email já cadastrados.')
                return render_template('register.html')

            # 3. Criação do utilizador via Model
            new_user = User()
            new_user.username = user_data.username
            new_user.email = user_data.email
            new_user.set_password(user_data.password)
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Conta criada com sucesso! Faça o login.')
            return redirect(url_for('auth.login'))

        except ValidationError as e:
            # Captura erros do Pydantic (ex: senha curta, email inválido)
            for error in e.errors():
                flash(f"Erro no campo {error['loc'][0]}: {error['msg']}")
        except Exception as e:
            db.session.rollback()
            flash('Ocorreu um erro interno. Tente novamente.')

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            # Redireciona para a página que o user tentou aceder originalmente (next)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        
        flash('Credenciais inválidas. Verifique o usuário e a senha.')
        
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
