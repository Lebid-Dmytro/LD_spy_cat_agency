Quick Start


# Clone the repository
git clone https://github.com/Lebid-Dmytro/LD_spy_cat_agency.git

cd LD_spy_cat_agency

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Load test data
python seed.py

# Start server
python manage.py runserver

# Open
# http://127.0.0.1:8000/api/docs/#/
