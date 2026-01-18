from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_required
from app.models import ATM
from app import db
from sqlalchemy import text

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    return render_template('index.html')

@main_bp.route('/api/atms')
@login_required
def get_atms():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    search = request.args.get('search', '')

    # Query SQL para calcular distância em KM
    sql = text("""
        SELECT *, (6371 * acos(cos(radians(:lat)) * cos(radians(latitude)) * cos(radians(longitude) - radians(:lon)) + sin(radians(:lat)) * sin(radians(latitude)))) AS distance 
        FROM atm 
        WHERE bank_name ILIKE :search
        ORDER BY distance ASC
    """)
    
    results = db.session.execute(sql, {'lat': lat, 'lon': lon, 'search': f'%{search}%'})
    
    atms = []
    for row in results:
        atms.append({
            "id": row.id,
            "bank_name": row.bank_name,
            "address": row.address,
            "distance": round(row.distance, 2),
            "lat": row.latitude,
            "lon": row.longitude
        })
    
    return jsonify(atms)

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('user_dashboard.html', user=current_user)