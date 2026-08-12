from app.db.database import create_tables
from app.db.models import Document


create_tables()

print("Database tables created successfully.")