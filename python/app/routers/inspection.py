from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime
from ..database import get_db
from ..models.database import Inspection
from pydantic import BaseModel
from fastapi.responses import FileResponse
from pathlib import Path
from ..utils.pdf_generator import PDFGenerator
import json
import os

router = APIRouter()
pdf_generator = PDFGenerator()

class InspectionCreate(BaseModel):
    inspector_id: str
    animal_id: str
    notes: str | None = None

class InspectionUpdate(BaseModel):
    status: str | None = None
    notes: str | None = None

class InspectionResponse(BaseModel):
    id: int
    timestamp: datetime
    inspector_id: str
    animal_id: str
    status: str
    notes: str | None = None

    class Config:
        from_attributes = True

@router.post("/", response_model=InspectionResponse)
async def create_inspection(
    inspection: InspectionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new inspection session"""
    db_inspection = Inspection(
        inspector_id=inspection.inspector_id,
        animal_id=inspection.animal_id,
        notes=inspection.notes,
        status="in_progress"
    )
    db.add(db_inspection)
    await db.commit()
    await db.refresh(db_inspection)
    return db_inspection

@router.get("/{inspection_id}", response_model=InspectionResponse)
async def get_inspection(
    inspection_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific inspection by ID"""
    result = await db.get(Inspection, inspection_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inspection not found"
        )
    return result

@router.put("/{inspection_id}", response_model=InspectionResponse)
async def update_inspection(
    inspection_id: int,
    inspection: InspectionUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an inspection's status or notes"""
    db_inspection = await db.get(Inspection, inspection_id)
    if db_inspection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inspection not found"
        )
    
    if inspection.status is not None:
        db_inspection.status = inspection.status
    if inspection.notes is not None:
        db_inspection.notes = inspection.notes
    
    await db.commit()
    await db.refresh(db_inspection)
    return db_inspection

@router.get("/", response_model=List[InspectionResponse])
async def list_inspections(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """List all inspections with pagination"""
    from sqlalchemy import select
    
    query = select(Inspection).offset(skip).limit(limit)
    result = await db.execute(query)
    inspections = result.scalars().all()
    return list(inspections)

@router.get("/report/{inspection_id}")
async def get_inspection_report(inspection_id: str):
    """Generate and return a PDF report for a specific inspection"""
    try:
        # Get inspection data from storage
        inspection_file = Path(f"data/inspections/inspection_{inspection_id}.json")
        if not inspection_file.exists():
            raise HTTPException(status_code=404, detail="Inspection not found")

        with open(inspection_file, 'r') as f:
            inspection_data = json.load(f)

        # Create reports directory if it doesn't exist
        reports_dir = Path("data/reports")
        reports_dir.mkdir(parents=True, exist_ok=True)

        # Generate PDF
        pdf_path = reports_dir / f"inspection_report_{inspection_id}.pdf"
        pdf_generator.generate_inspection_report(inspection_data, str(pdf_path))

        # Return the PDF file
        return FileResponse(
            path=pdf_path,
            filename=f"inspection_report_{inspection_id}.pdf",
            media_type="application/pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/monthly-report/{year}/{month}")
async def get_monthly_report(year: int, month: int):
    """Generate and return a PDF report for a specific month"""
    try:
        # Validate month
        if month < 1 or month > 12:
            raise HTTPException(status_code=400, detail="Invalid month")

        # Get all inspections for the month
        inspections_dir = Path("data/inspections")
        month_data = {
            'month': f"{year}-{month:02d}",
            'total_inspections': 0,
            'passed_inspections': 0,
            'failed_inspections': 0,
            'pending_actions': 0,
            'inspections': []
        }

        # Collect inspection data for the month
        if inspections_dir.exists():
            for file in inspections_dir.glob("inspection_*.json"):
                with open(file, 'r') as f:
                    inspection = json.load(f)
                    inspection_date = datetime.strptime(inspection['date'], '%Y-%m-%d')
                    
                    if inspection_date.year == year and inspection_date.month == month:
                        month_data['total_inspections'] += 1
                        if inspection['health_status'] == 'Passed':
                            month_data['passed_inspections'] += 1
                        elif inspection['health_status'] == 'Failed':
                            month_data['failed_inspections'] += 1
                        if inspection.get('pending_actions', False):
                            month_data['pending_actions'] += 1
                        
                        month_data['inspections'].append({
                            'date': inspection['date'],
                            'id': inspection['id'],
                            'animal_type': inspection['animal_type'],
                            'status': inspection['health_status']
                        })

        # Sort inspections by date
        month_data['inspections'].sort(key=lambda x: x['date'])

        # Create reports directory if it doesn't exist
        reports_dir = Path("data/reports")
        reports_dir.mkdir(parents=True, exist_ok=True)

        # Generate PDF
        pdf_path = reports_dir / f"monthly_report_{year}_{month:02d}.pdf"
        pdf_generator.generate_monthly_report(month_data, str(pdf_path))

        # Return the PDF file
        return FileResponse(
            path=pdf_path,
            filename=f"monthly_report_{year}_{month:02d}.pdf",
            media_type="application/pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 