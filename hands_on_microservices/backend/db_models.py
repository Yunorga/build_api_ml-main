from sqlalchemy import Column, Integer, String, LargeBinary
from database import Base

class ImageRecord(Base):
    """
    Table qui stocke les images et la forme prédite.
    """
    __tablename__ = "images"

    # id = 1
    # image_data = b"fake_data"
    # predicted_shape = "circle"


    id = Column(Integer, primary_key=True, index=True)
    image_data = Column(LargeBinary, nullable=False)
    predicted_shape = Column(String, nullable=False)



