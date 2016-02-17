from app import app
from models import create_tables

if __name__ == "__main__":
    create_tables()
    app.run(debug=app.config.get("DEBUG", False))
