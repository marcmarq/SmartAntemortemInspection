from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import cv2
import numpy as np
from datetime import datetime
from ..database import get_db
from ..models.database import Detection, Inspection
from pydantic import BaseModel

router = APIRouter()

class DetectionCreate(BaseModel):
    inspection_id: int
    lesion_type: str
    confidence_score: float
    location_data: dict

class DetectionUpdate(BaseModel):
    verified: bool
    verified_by: str | None = None

class DetectionResponse(BaseModel):
    id: int
    inspection_id: int
    timestamp: datetime
    lesion_type: str
    confidence_score: float
    location_data: dict
    verified: bool
    verified_by: str | None = None

    class Config:
        from_attributes = True

class DetectionSettings(BaseModel):
    confidence_threshold: float = 0.5
    min_detection_size: int = 20
    max_detection_size: int = 200
    processing_interval: int = 100

@router.post("/process", response_model=List[DetectionResponse])
async def process_image(
    inspection_id: int,
    file: UploadFile = File(...),
    settings: DetectionSettings = DetectionSettings(),
    db: AsyncSession = Depends(get_db)
):
    """Process an image for lesion detection"""
    # Verify inspection exists
    inspection = await db.get(Inspection, inspection_id)
    if inspection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inspection not found"
        )

    # Read and process image
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image format"
        )

    # TODO: Implement actual detection logic using TensorFlow/Keras model
    # For now, return dummy detection
    dummy_detection = Detection(
        inspection_id=inspection_id,
        lesion_type="sample_lesion",
        confidence_score=0.85,
        location_data={
            "x": 100,
            "y": 100,
            "width": 50,
            "height": 50
        },
        verified=False
    )
    
    db.add(dummy_detection)
    await db.commit()
    await db.refresh(dummy_detection)
    
    return [dummy_detection]

@router.get("/inspection/{inspection_id}", response_model=List[DetectionResponse])
async def list_detections(
    inspection_id: int,
    db: AsyncSession = Depends(get_db)
):
    """List all detections for a specific inspection"""
    from sqlalchemy import select
    
    query = select(Detection).where(Detection.inspection_id == inspection_id)
    result = await db.execute(query)
    detections = result.scalars().all()
    return list(detections)

@router.put("/{detection_id}", response_model=DetectionResponse)
async def verify_detection(
    detection_id: int,
    update: DetectionUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Verify or update a detection"""
    detection = await db.get(Detection, detection_id)
    if detection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Detection not found"
        )
    
    detection.verified = update.verified
    detection.verified_by = update.verified_by
    
    await db.commit()
    await db.refresh(detection)
    return detection

@router.delete("/{detection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_detection(
    detection_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a detection"""
    detection = await db.get(Detection, detection_id)
    if detection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Detection not found"
        )
    
    await db.delete(detection)
    await db.commit() 