from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.schemas.user_schema import UserCreate
from app import db, mail
from flask_mail import Message
from pydantic import ValidationError

auth_bp = Blueprint('auth', __name__)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    msg = Message('Solicitação de Redefinição de Senha',
                sender='noreply@demo.com',
                recipients=[user.email])
    msg.body = f'''Para redefinir sua senha, visite o seguinte link:
{url_for('auth.reset_password', token=token, _external=True)}

Se você não fez esta solicitação, simplesmente ignore este email e nenhuma alteração será feita.
'''
    mail.send(msg)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))


    if request.method == 'POST':
        try:
            if request.form.get('password') != request.form.get('confirm_password'):
                flash('As senhas não coincidem.')
                return render_template('register.html')

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
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            # Redireciona para a página que o user tentou aceder originalmente (next)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        
        flash('Credenciais inválidas. Verifique o email e a senha.')
        
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.username = request.form.get('username')
        current_user.email = request.form.get('email')
        db.session.commit()
        flash('Seu perfil foi atualizado com sucesso!')
        return redirect(url_for('main.user_dashboard'))
    return render_template('edit_profile.html', user=current_user)

@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not current_user.check_password(current_password):
            flash('A senha atual está incorreta.')
        elif new_password != confirm_password:
            flash('As novas senhas não coincidem.')
        else:
            current_user.set_password(new_password)
            db.session.commit()
            flash('Sua senha foi alterada com sucesso!')
            return redirect(url_for('main.user_dashboard'))
            
    return render_template('change_password.html')

@auth_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            send_password_reset_email(user)
        flash('Verifique seu email para as instruções de redefinição de senha.')
        return redirect(url_for('auth.login'))
    return render_template('reset_password_request.html')

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash('Senhas não coincidem.')
            return redirect(url_for('auth.reset_password', token=token))
        user.set_password(password)
        db.session.commit()
        flash('Sua senha foi redefinida com sucesso.')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html')

@auth_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    flash('Sua conta foi eliminada com sucesso.')
    return redirect(url_for('auth.login'))
