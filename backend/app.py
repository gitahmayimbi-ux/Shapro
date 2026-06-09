from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///shapro.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

db = SQLAlchemy(app)

# Models
class Farm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    area_hectares = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'area_hectares': self.area_hectares
        }

class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    rainfall = db.Column(db.Float, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'rainfall': self.rainfall,
            'wind_speed': self.wind_speed,
            'recorded_at': self.recorded_at.isoformat()
        }

class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'), nullable=False)
    crop_name = db.Column(db.String(100), nullable=False)
    planting_date = db.Column(db.DateTime, nullable=False)
    expected_harvest = db.Column(db.DateTime, nullable=False)
    area_planted = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='growing')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'crop_name': self.crop_name,
            'planting_date': self.planting_date.isoformat(),
            'expected_harvest': self.expected_harvest.isoformat(),
            'area_planted': self.area_planted,
            'status': self.status
        }

# Routes
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'status': 'success',
        'message': 'Shapro - Smart Agro-Climatic System API',
        'version': '1.0.0',
        'endpoints': {
            'farms': '/api/farms',
            'weather': '/api/weather',
            'crops': '/api/crops',
            'recommendations': '/api/recommendations',
            'analytics': '/api/analytics'
        }
    })

@app.route('/api/farms', methods=['GET', 'POST'])
def farms():
    if request.method == 'POST':
        data = request.get_json()
        farm = Farm(
            name=data.get('name'),
            location=data.get('location'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            area_hectares=data.get('area_hectares')
        )
        db.session.add(farm)
        db.session.commit()
        return jsonify(farm.to_dict()), 201
    else:
        farms = Farm.query.all()
        return jsonify([farm.to_dict() for farm in farms])

@app.route('/api/weather/<int:farm_id>', methods=['GET'])
def get_weather(farm_id):
    weather_data = WeatherData.query.filter_by(farm_id=farm_id).order_by(WeatherData.recorded_at.desc()).limit(24).all()
    return jsonify([w.to_dict() for w in weather_data])

@app.route('/api/crops', methods=['GET', 'POST'])
def crops():
    if request.method == 'POST':
        data = request.get_json()
        crop = Crop(
            farm_id=data.get('farm_id'),
            crop_name=data.get('crop_name'),
            planting_date=datetime.fromisoformat(data.get('planting_date')),
            expected_harvest=datetime.fromisoformat(data.get('expected_harvest')),
            area_planted=data.get('area_planted')
        )
        db.session.add(crop)
        db.session.commit()
        return jsonify(crop.to_dict()), 201
    else:
        crops = Crop.query.all()
        return jsonify([crop.to_dict() for crop in crops])

@app.route('/api/recommendations', methods=['GET'])
def recommendations():
    farm_id = request.args.get('farm_id', type=int)
    
    recommendations = [
        {
            'type': 'planting',
            'crop': 'Maize',
            'confidence': 0.85,
            'reason': 'Optimal temperature and humidity detected'
        },
        {
            'type': 'irrigation',
            'crop': 'Tomato',
            'confidence': 0.92,
            'reason': 'Soil moisture below recommended threshold'
        },
        {
            'type': 'pest_alert',
            'crop': 'Wheat',
            'confidence': 0.78,
            'reason': 'High humidity may encourage fungal growth'
        }
    ]
    return jsonify(recommendations)

@app.route('/api/analytics', methods=['GET'])
def analytics():
    farm_id = request.args.get('farm_id', type=int)
    
    analytics = {
        'total_farms': Farm.query.count(),
        'total_crops': Crop.query.count(),
        'average_temperature': 24.5,
        'average_humidity': 65.2,
        'predicted_yield': 8500,
        'yield_unit': 'kg/hectare'
    }
    return jsonify(analytics)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
