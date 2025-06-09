from fastapi import APIRouter, Depends, HTTPException, status, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import cv2
import numpy as np
from ..database import get_db
from ..models.database import CameraConfig
from pydantic import BaseModel

router = APIRouter()

class CameraSettingsUpdate(BaseModel):
    resolution: str
    framerate: int
    settings: dict

class CameraResponse(BaseModel):
    id: int
    camera_id: str
    name: str
    settings: dict
    is_active: bool

    class Config:
        from_attributes = True

@router.get("/list", response_model=List[CameraResponse])
async def list_cameras(db: AsyncSession = Depends(get_db)):
    """List all configured cameras"""
    from sqlalchemy import select
    
    query = select(CameraConfig).where(CameraConfig.is_active == True)
    result = await db.execute(query)
    cameras = result.scalars().all()
    return list(cameras)

@router.post("/configure/{camera_id}", response_model=CameraResponse)
async def configure_camera(
    camera_id: str,
    settings: CameraSettingsUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Configure a camera with specific settings"""
    from sqlalchemy import select
    
    # Check if camera already exists
    query = select(CameraConfig).where(CameraConfig.camera_id == camera_id)
    result = await db.execute(query)
    camera = result.scalar_one_or_none()
    
    if camera is None:
        # Create new camera config
        camera = CameraConfig(
            camera_id=camera_id,
            name=f"Camera {camera_id}",
            settings={
                "resolution": settings.resolution,
                "framerate": settings.framerate,
                **settings.settings
            },
            is_active=True
        )
        db.add(camera)
    else:
        # Update existing camera config
        camera.settings = {
            "resolution": settings.resolution,
            "framerate": settings.framerate,
            **settings.settings
        }
    
    await db.commit()
    await db.refresh(camera)
    return camera

@router.delete("/{camera_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_camera(
    camera_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Remove a camera configuration"""
    from sqlalchemy import select
    
    query = select(CameraConfig).where(CameraConfig.camera_id == camera_id)
    result = await db.execute(query)
    camera = result.scalar_one_or_none()
    
    if camera is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )
    
    camera.is_active = False
    await db.commit()

class CameraManager:
    def __init__(self):
        self.active_cameras = {}

    async def start_camera(self, camera_id: str, settings: dict):
        """Start a camera capture"""
        if camera_id in self.active_cameras:
            return
        
        # Parse resolution
        width, height = map(int, settings["resolution"].split("x"))
        
        # Initialize camera
        cap = cv2.VideoCapture(int(camera_id))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        cap.set(cv2.CAP_PROP_FPS, settings["framerate"])
        
        self.active_cameras[camera_id] = cap

    async def stop_camera(self, camera_id: str):
        """Stop a camera capture"""
        if camera_id in self.active_cameras:
            self.active_cameras[camera_id].release()
            del self.active_cameras[camera_id]

    async def get_frame(self, camera_id: str) -> bytes:
        """Get a frame from the camera"""
        if camera_id not in self.active_cameras:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Camera not active"
            )
        
        cap = self.active_cameras[camera_id]
        ret, frame = cap.read()
        
        if not ret:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to capture frame"
            )
        
        # Convert frame to JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        return buffer.tobytes()

camera_manager = CameraManager()

@router.websocket("/stream/{camera_id}")
async def stream_camera(
    websocket: WebSocket,
    camera_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Stream camera feed over WebSocket"""
    await websocket.accept()
    
    try:
        # Get camera settings
        query = select(CameraConfig).where(CameraConfig.camera_id == camera_id)
        result = await db.execute(query)
        camera = result.scalar_one_or_none()
        
        if camera is None:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        
        # Start camera
        await camera_manager.start_camera(camera_id, camera.settings)
        
        while True:
            try:
                frame = await camera_manager.get_frame(camera_id)
                await websocket.send_bytes(frame)
            except Exception as e:
                print(f"Error streaming frame: {e}")
                break
    
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await camera_manager.stop_camera(camera_id)
        await websocket.close() 