import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.database import get_db
from app.models.database import Inspection

# Test data
test_inspection = {
    "inspector_id": "test_inspector",
    "animal_id": "test_animal",
    "notes": "Test inspection"
}

@pytest.mark.asyncio
async def test_create_inspection(async_client: AsyncClient):
    """Test creating a new inspection"""
    response = await async_client.post("/api/inspection/", json=test_inspection)
    assert response.status_code == 200
    data = response.json()
    assert data["inspector_id"] == test_inspection["inspector_id"]
    assert data["animal_id"] == test_inspection["animal_id"]
    assert data["status"] == "in_progress"

@pytest.mark.asyncio
async def test_get_inspection(async_client: AsyncClient, test_db: AsyncSession):
    """Test getting a specific inspection"""
    # Create test inspection
    inspection = Inspection(**test_inspection, status="in_progress")
    test_db.add(inspection)
    await test_db.commit()
    await test_db.refresh(inspection)

    response = await async_client.get(f"/api/inspection/{inspection.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == inspection.id
    assert data["inspector_id"] == inspection.inspector_id

@pytest.mark.asyncio
async def test_update_inspection(async_client: AsyncClient, test_db: AsyncSession):
    """Test updating an inspection"""
    # Create test inspection
    inspection = Inspection(**test_inspection, status="in_progress")
    test_db.add(inspection)
    await test_db.commit()
    await test_db.refresh(inspection)

    update_data = {
        "status": "completed",
        "notes": "Updated notes"
    }
    response = await async_client.put(
        f"/api/inspection/{inspection.id}",
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["notes"] == "Updated notes"

@pytest.mark.asyncio
async def test_list_inspections(async_client: AsyncClient, test_db: AsyncSession):
    """Test listing inspections"""
    # Create test inspections
    inspections = [
        Inspection(**test_inspection, status="in_progress"),
        Inspection(**test_inspection, status="completed")
    ]
    for inspection in inspections:
        test_db.add(inspection)
    await test_db.commit()

    response = await async_client.get("/api/inspection/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

@pytest.fixture
async def async_client():
    """Async client fixture"""
    from fastapi.testclient import TestClient
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def test_db():
    """Test database fixture"""
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback() 