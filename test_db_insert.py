from uuid import uuid4

from app.db.database import SessionLocal
from app.db.models import Document


db = SessionLocal()

try:
    document = Document(
        document_id=uuid4(),
        filename="test.txt",
        file_type="txt",
        file_size=1234,
        chunking_strategy="recursive",
        chunk_count=10,
    )

    db.add(document)
    db.commit()

    print("Document inserted successfully.")

finally:
    db.close()