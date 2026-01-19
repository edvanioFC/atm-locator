from typing import Optional
from app import db

class ATM(db.Model):
    table_name = 'atms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bank_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    # Adicione o construtor explicitamente para o Pylance
    def __init__(self, bank_name: str, latitude: float, longitude: float, address: Optional[str] = None, is_active: bool = True):
        self.bank_name = bank_name
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.is_active = is_active

    def __repr__(self):
        return f'<ATM {self.bank_name}>'