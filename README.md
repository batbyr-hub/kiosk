# Kiosk 🖥️📱

A self-service telecom kiosk system developed with Django and deployed on both Windows and Android platforms. Designed for customer independence and efficiency, especially during the COVID-19 period.

## ✨ Highlights

- Works seamlessly on both desktop (Windows) and Android environments
- Handles customer service tasks with minimal staff interaction
- Used in real-world telecom operations
- Offline-compatible mode for certain deployments

## 🏗️ Tech Stack

- Python 3.x
- Django
- MySQL
- HTML / CSS / JavaScript
- WebSocket
- Windows & Android compatibility

## 📦 Setup Instructions

```bash
git clone https://github.com/batbyr-hub/kiosk.git
cd kiosk
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
