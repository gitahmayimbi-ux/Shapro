const API_BASE_URL = 'http://localhost:5000/api';

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
    loadFarms();
    setupFarmForm();
    setupCropForm();
    loadRecommendations();
    loadAnalytics();
});

// Dashboard
async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE_URL}/analytics`);
        const data = await response.json();
        
        document.getElementById('totalFarms').textContent = data.total_farms;
        document.getElementById('activeCrops').textContent = data.total_crops;
        document.getElementById('avgTemp').textContent = data.average_temperature.toFixed(1);
        
        // Mock weather data
        document.getElementById('weatherTemp').textContent = '24°C';
        document.getElementById('weatherHumidity').textContent = '65';
        document.getElementById('weatherWind').textContent = '2.5';
        document.getElementById('weatherStatus').textContent = 'Partly Cloudy';
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// Farms Management
async function loadFarms() {
    try {
        const response = await fetch(`${API_BASE_URL}/farms`);
        const farms = await response.json();
        
        const farmsList = document.getElementById('farmsList');
        farmsList.innerHTML = '';
        
        farms.forEach(farm => {
            const farmCard = document.createElement('div');
            farmCard.className = 'farm-item';
            farmCard.innerHTML = `
                <h4>${farm.name}</h4>
                <p><strong>Location:</strong> ${farm.location}</p>
                <p><strong>Coordinates:</strong> ${farm.latitude.toFixed(4)}, ${farm.longitude.toFixed(4)}</p>
                <p><strong>Area:</strong> ${farm.area_hectares} hectares</p>
            `;
            farmsList.appendChild(farmCard);
        });
        
        // Update crop form farm dropdown
        const farmSelect = document.getElementById('cropFarm');
        farms.forEach(farm => {
            const option = document.createElement('option');
            option.value = farm.id;
            option.textContent = farm.name;
            farmSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading farms:', error);
    }
}

function setupFarmForm() {
    const form = document.getElementById('farmForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const farmData = {
            name: document.getElementById('farmName').value,
            location: document.getElementById('farmLocation').value,
            latitude: parseFloat(document.getElementById('farmLat').value),
            longitude: parseFloat(document.getElementById('farmLon').value),
            area_hectares: parseFloat(document.getElementById('farmArea').value)
        };
        
        try {
            const response = await fetch(`${API_BASE_URL}/farms`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(farmData)
            });
            
            if (response.ok) {
                alert('Farm added successfully!');
                form.reset();
                loadFarms();
            } else {
                alert('Error adding farm');
            }
        } catch (error) {
            console.error('Error adding farm:', error);
            alert('Error adding farm');
        }
    });
}

// Crops Management
async function loadCrops() {
    try {
        const response = await fetch(`${API_BASE_URL}/crops`);
        const crops = await response.json();
        
        const cropsList = document.getElementById('cropsList');
        cropsList.innerHTML = '';
        
        crops.forEach(crop => {
            const cropCard = document.createElement('div');
            cropCard.className = 'crop-item';
            cropCard.innerHTML = `
                <h4>${crop.crop_name}</h4>
                <p><strong>Farm ID:</strong> ${crop.farm_id}</p>
                <p><strong>Planted:</strong> ${new Date(crop.planting_date).toLocaleDateString()}</p>
                <p><strong>Harvest:</strong> ${new Date(crop.expected_harvest).toLocaleDateString()}</p>
                <p><strong>Area:</strong> ${crop.area_planted} hectares</p>
                <p><strong>Status:</strong> <span class="recommendation-badge">${crop.status}</span></p>
            `;
            cropsList.appendChild(cropCard);
        });
    } catch (error) {
        console.error('Error loading crops:', error);
    }
}

function setupCropForm() {
    const form = document.getElementById('cropForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const cropData = {
            farm_id: parseInt(document.getElementById('cropFarm').value),
            crop_name: document.getElementById('cropName').value,
            planting_date: new Date(document.getElementById('cropPlanting').value).toISOString(),
            expected_harvest: new Date(document.getElementById('cropHarvest').value).toISOString(),
            area_planted: parseFloat(document.getElementById('cropArea').value)
        };
        
        try {
            const response = await fetch(`${API_BASE_URL}/crops`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(cropData)
            });
            
            if (response.ok) {
                alert('Crop added successfully!');
                form.reset();
                loadCrops();
            } else {
                alert('Error adding crop');
            }
        } catch (error) {
            console.error('Error adding crop:', error);
            alert('Error adding crop');
        }
    });
}

// Recommendations
async function loadRecommendations() {
    try {
        const response = await fetch(`${API_BASE_URL}/recommendations`);
        const recommendations = await response.json();
        
        const recList = document.getElementById('recommendationsList');
        recList.innerHTML = '';
        
        recommendations.forEach(rec => {
            const recCard = document.createElement('div');
            const isPriority = rec.confidence > 0.8;
            recCard.className = `recommendation-item ${isPriority ? 'high-priority' : ''}`;
            
            const emoji = rec.type === 'planting' ? '🌱' : rec.type === 'irrigation' ? '💧' : '🐛';
            
            recCard.innerHTML = `
                <h4>${emoji} ${rec.type.toUpperCase()}</h4>
                <p><strong>Crop:</strong> ${rec.crop}</p>
                <p><strong>Reason:</strong> ${rec.reason}</p>
                <p><strong>Confidence:</strong> <span class="recommendation-badge">${(rec.confidence * 100).toFixed(0)}%</span></p>
            `;
            recList.appendChild(recCard);
        });
    } catch (error) {
        console.error('Error loading recommendations:', error);
    }
}

// Analytics
function loadAnalytics() {
    // Temperature Chart
    const tempCtx = document.getElementById('tempChart').getContext('2d');
    new Chart(tempCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'Temperature (°C)',
                data: [18, 19, 21, 24, 27, 29, 30, 29, 27, 24, 21, 19],
                borderColor: '#e74c3c',
                backgroundColor: 'rgba(231, 76, 60, 0.1)',
                borderWidth: 2,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    
    // Humidity Chart
    const humidityCtx = document.getElementById('humidityChart').getContext('2d');
    new Chart(humidityCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'Humidity (%)',
                data: [65, 63, 60, 58, 62, 68, 72, 70, 67, 61, 64, 66],
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                borderWidth: 2,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}
