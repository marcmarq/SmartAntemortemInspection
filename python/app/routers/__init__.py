"""
FastAPI routers for the Antemortem Inspection Application
"""

from . import inspection
from . import camera
from . import detection

__all__ = ['inspection', 'camera', 'detection'] 