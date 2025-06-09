# Smart Antemortem Inspection App

A desktop application for automated lesion detection and inspection management using computer vision and deep learning.

## Technology Stack

### Frontend
- Electron + React
- TailwindCSS
- TypeScript
- Vite

### Backend
- FastAPI (Python)
- OpenCV for image processing
- TensorFlow/Keras for deep learning
- SQLite with SQLAlchemy ORM

## Project Structure
```
antemortem-inspection-app/
├── python/              # Backend service
│   ├── app/            # FastAPI application
│   ├── models/         # ML models and SQLAlchemy models
│   ├── services/       # Business logic
│   ├── utils/          # Helper functions
│   └── tests/          # Backend tests
├── src/                # Frontend source
│   ├── components/     # React components
│   ├── pages/          # Page components
│   ├── services/       # Frontend services
│   ├── utils/          # Helper functions
│   └── types/          # TypeScript types
├── public/             # Static assets
└── electron/           # Electron main process code
```

## Development Setup

### Prerequisites
- Node.js 18+
- Python 3.10+
- CUDA-capable GPU (optional, for ML acceleration)

### Backend Setup
1. Navigate to the python directory:
   ```bash
   cd python
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup
1. Install dependencies:
   ```bash
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```

## Features
- Real-time camera feed display
- Region of interest (ROI) selection
- Multiple camera support
- Lesion detection using deep learning
- Inspection session recording
- Historical data viewing
- Export functionality (PDF, CSV)
- Backup and restore capabilities

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details. 