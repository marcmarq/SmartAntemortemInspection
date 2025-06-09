from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    inspector_id = Column(String, index=True)
    animal_id = Column(String, index=True)
    status = Column(String)  # e.g., "completed", "in_progress", "cancelled"
    notes = Column(String, nullable=True)
    
    # Relationships
    detections = relationship("Detection", back_populates="inspection")
    images = relationship("Image", back_populates="inspection")

class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    lesion_type = Column(String)
    confidence_score = Column(Float)
    location_data = Column(JSON)  # Stores coordinates and region info
    verified = Column(Boolean, default=False)
    verified_by = Column(String, nullable=True)
    
    # Relationships
    inspection = relationship("Inspection", back_populates="detections")
    image = relationship("Image", back_populates="detections")

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"))
    file_path = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    camera_id = Column(String)
    metadata = Column(JSON, nullable=True)  # Stores camera settings, resolution, etc.
    
    # Relationships
    inspection = relationship("Inspection", back_populates="images")
    detections = relationship("Detection", back_populates="image")

class CameraConfig(Base):
    __tablename__ = "camera_configs"

    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(String, unique=True, index=True)
    name = Column(String)
    settings = Column(JSON)  # Stores camera-specific settings
    is_active = Column(Boolean, default=True)
    last_updated = Column(DateTime, default=datetime.utcnow)

class SystemConfig(Base):
    __tablename__ = "system_configs"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(JSON)
    description = Column(String, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow) 