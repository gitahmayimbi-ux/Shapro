import json
from datetime import datetime, timedelta

class CropModel:
    """
    Machine learning model for crop recommendations and yield prediction
    """
    
    # Crop requirements database
    CROP_REQUIREMENTS = {
        'maize': {
            'optimal_temp': (18, 28),
            'optimal_humidity': (60, 75),
            'optimal_rainfall': (50, 100),
            'growing_days': 120,
            'pest_risk_high_humidity': 70
        },
        'wheat': {
            'optimal_temp': (12, 22),
            'optimal_humidity': (50, 70),
            'optimal_rainfall': (30, 60),
            'growing_days': 150,
            'pest_risk_high_humidity': 75
        },
        'rice': {
            'optimal_temp': (20, 30),
            'optimal_humidity': (75, 85),
            'optimal_rainfall': (100, 200),
            'growing_days': 120,
            'pest_risk_high_humidity': 80
        },
        'tomato': {
            'optimal_temp': (15, 25),
            'optimal_humidity': (60, 70),
            'optimal_rainfall': (40, 80),
            'growing_days': 80,
            'pest_risk_high_humidity': 75
        }
    }
    
    def __init__(self):
        pass
    
    @staticmethod
    def calculate_suitability_score(crop_name, temperature, humidity, rainfall):
        """
        Calculate how suitable current conditions are for a crop
        Returns score 0-100
        """
        if crop_name.lower() not in CropModel.CROP_REQUIREMENTS:
            return 0
        
        requirements = CropModel.CROP_REQUIREMENTS[crop_name.lower()]
        
        # Temperature score
        temp_min, temp_max = requirements['optimal_temp']
        if temp_min <= temperature <= temp_max:
            temp_score = 100
        elif temp_min - 5 <= temperature <= temp_max + 5:
            temp_score = 70
        else:
            temp_score = 30
        
        # Humidity score
        hum_min, hum_max = requirements['optimal_humidity']
        if hum_min <= humidity <= hum_max:
            hum_score = 100
        elif hum_min - 10 <= humidity <= hum_max + 10:
            hum_score = 70
        else:
            hum_score = 30
        
        # Rainfall score
        rain_min, rain_max = requirements['optimal_rainfall']
        if rain_min <= rainfall <= rain_max:
            rain_score = 100
        elif rain_min - 20 <= rainfall <= rain_max + 20:
            rain_score = 70
        else:
            rain_score = 30
        
        # Overall weighted score
        overall = (temp_score * 0.4 + hum_score * 0.3 + rain_score * 0.3)
        return overall
    
    @staticmethod
    def predict_yield(crop_name, area_hectares, temperature, humidity, rainfall, growing_days_elapsed):
        """
        Predict crop yield based on weather and growth conditions
        Returns yield in kg
        """
        # Base yields per hectare (kg/ha) - these are approximate values
        base_yields = {
            'maize': 4000,
            'wheat': 3000,
            'rice': 5000,
            'tomato': 20000
        }
        
        base_yield = base_yields.get(crop_name.lower(), 3000)
        suitability = CropModel.calculate_suitability_score(crop_name, temperature, humidity, rainfall)
        
        # Yield prediction: base yield * suitability factor * growth progress
        growth_progress = min(1.0, growing_days_elapsed / 120)  # 120 days average
        predicted_yield = base_yield * (suitability / 100) * growth_progress * area_hectares
        
        return predicted_yield
    
    @staticmethod
    def get_recommendations(crop_name, temperature, humidity, rainfall, soil_moisture):
        """
        Generate actionable farming recommendations
        """
        recommendations = []
        
        if crop_name.lower() not in CropModel.CROP_REQUIREMENTS:
            return recommendations
        
        requirements = CropModel.CROP_REQUIREMENTS[crop_name.lower()]
        
        # Temperature recommendations
        temp_min, temp_max = requirements['optimal_temp']
        if temperature < temp_min:
            recommendations.append({
                'type': 'temperature',
                'severity': 'warning',
                'message': f'Temperature is below optimal. Current: {temperature}°C, Optimal: {temp_min}-{temp_max}°C'
            })
        elif temperature > temp_max:
            recommendations.append({
                'type': 'temperature',
                'severity': 'warning',
                'message': f'Temperature is above optimal. Current: {temperature}°C, Optimal: {temp_min}-{temp_max}°C'
            })
        
        # Humidity and pest recommendations
        pest_risk = requirements['pest_risk_high_humidity']
        if humidity > pest_risk:
            recommendations.append({
                'type': 'pest_alert',
                'severity': 'danger',
                'message': f'High humidity ({humidity}%) increases pest and disease risk. Consider spraying fungicide.'
            })
        
        # Irrigation recommendations
        if soil_moisture < 30:
            recommendations.append({
                'type': 'irrigation',
                'severity': 'danger',
                'message': f'Soil moisture is low ({soil_moisture}%). Irrigation needed immediately.'
            })
        elif soil_moisture < 50:
            recommendations.append({
                'type': 'irrigation',
                'severity': 'warning',
                'message': f'Soil moisture is below optimal ({soil_moisture}%). Plan irrigation soon.'
            })
        
        # Rainfall recommendations
        rain_min, rain_max = requirements['optimal_rainfall']
        if rainfall < rain_min:
            recommendations.append({
                'type': 'water_management',
                'severity': 'warning',
                'message': f'Rainfall is below optimal ({rainfall}mm). Supplement with irrigation.'
            })
        
        return recommendations
    
    @staticmethod
    def estimate_harvest_date(crop_name, planting_date, current_conditions_avg_suitability):
        """
        Estimate harvest date based on crop and current conditions
        """
        if crop_name.lower() not in CropModel.CROP_REQUIREMENTS:
            return None
        
        base_growing_days = CropModel.CROP_REQUIREMENTS[crop_name.lower()]['growing_days']
        
        # Adjust growing days based on conditions
        # Lower suitability = longer growing period
        suitability_factor = current_conditions_avg_suitability / 100
        adjusted_days = base_growing_days / suitability_factor if suitability_factor > 0 else base_growing_days
        
        harvest_date = planting_date + timedelta(days=adjusted_days)
        return harvest_date
