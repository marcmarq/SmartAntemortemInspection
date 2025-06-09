import { useState, useEffect, useRef } from 'react'
import Webcam from 'react-webcam'
import { useParams } from 'react-router-dom'
import ReportActions from '../components/ReportActions'

interface Detection {
  id: string
  type: string
  confidence: number
  bbox: [number, number, number, number] // [x, y, width, height]
  timestamp: string
}

const Inspection: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const webcamRef = useRef<Webcam>(null)
  const [isRecording, setIsRecording] = useState(false)
  const [detections, setDetections] = useState<Detection[]>([])
  const [selectedCamera, setSelectedCamera] = useState<string>('')
  const [cameras, setCameras] = useState<MediaDeviceInfo[]>([])
  const [inspectionData, setInspectionData] = useState(null)

  useEffect(() => {
    // Get list of available cameras
    navigator.mediaDevices.enumerateDevices()
      .then(devices => {
        const videoDevices = devices.filter(device => device.kind === 'videoinput')
        setCameras(videoDevices)
        if (videoDevices.length > 0) {
          setSelectedCamera(videoDevices[0].deviceId)
        }
      })
      .catch(err => {
        console.error("Error accessing cameras:", err)
      })
  }, [])

  const startInspection = () => {
    setIsRecording(true)
    // TODO: Start sending frames to backend for processing
  }

  const stopInspection = () => {
    setIsRecording(false)
    // TODO: Stop processing and save inspection data
  }

  const captureFrame = () => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot()
      // TODO: Send frame to backend for processing
      console.log("Captured frame:", imageSrc?.slice(0, 50) + "...")
    }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Inspection Details</h1>
        {id && <ReportActions inspectionId={id} />}
      </div>

      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-3xl font-bold tracking-tight">Live Inspection</h2>
          <div className="flex items-center space-x-4">
            <select
              value={selectedCamera}
              onChange={(e) => setSelectedCamera(e.target.value)}
              className="rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
            >
              {cameras.map(camera => (
                <option key={camera.deviceId} value={camera.deviceId}>
                  {camera.label || `Camera ${camera.deviceId.slice(0, 5)}...`}
                </option>
              ))}
            </select>
            <button
              onClick={isRecording ? stopInspection : startInspection}
              className={`inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring h-9 px-4 py-2 ${
                isRecording
                  ? 'bg-destructive text-destructive-foreground hover:bg-destructive/90'
                  : 'bg-primary text-primary-foreground hover:bg-primary/90'
              }`}
            >
              {isRecording ? 'Stop Inspection' : 'Start Inspection'}
            </button>
          </div>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          {/* Camera Feed */}
          <div className="rounded-lg border bg-card text-card-foreground shadow-sm">
            <div className="p-6">
              <h3 className="text-lg font-medium mb-4">Camera Feed</h3>
              <div className="relative aspect-video bg-muted rounded-md overflow-hidden">
                <Webcam
                  ref={webcamRef}
                  audio={false}
                  videoConstraints={{
                    deviceId: selectedCamera,
                    width: 1280,
                    height: 720
                  }}
                  className="w-full h-full object-cover"
                />
              </div>
            </div>
          </div>

          {/* Detections List */}
          <div className="rounded-lg border bg-card text-card-foreground shadow-sm">
            <div className="p-6">
              <h3 className="text-lg font-medium mb-4">Detected Lesions</h3>
              <div className="space-y-4">
                {detections.length === 0 ? (
                  <p className="text-sm text-muted-foreground">
                    No lesions detected yet. Start the inspection to begin detection.
                  </p>
                ) : (
                  detections.map(detection => (
                    <div
                      key={detection.id}
                      className="flex items-center justify-between p-4 rounded-md border"
                    >
                      <div>
                        <p className="font-medium">{detection.type}</p>
                        <p className="text-sm text-muted-foreground">
                          Confidence: {(detection.confidence * 100).toFixed(1)}%
                        </p>
                      </div>
                      <span className="text-xs text-muted-foreground">
                        {new Date(detection.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Inspection 