import { useState, useEffect } from 'react'

interface CameraSettings {
  deviceId: string
  name: string
  resolution: string
  framerate: number
}

interface DetectionSettings {
  confidenceThreshold: number
  minDetectionSize: number
  maxDetectionSize: number
  processingInterval: number
}

export default function Settings() {
  const [cameraSettings, setCameraSettings] = useState<CameraSettings>({
    deviceId: '',
    name: '',
    resolution: '1280x720',
    framerate: 30
  })

  const [detectionSettings, setDetectionSettings] = useState<DetectionSettings>({
    confidenceThreshold: 0.5,
    minDetectionSize: 20,
    maxDetectionSize: 200,
    processingInterval: 100
  })

  const handleSaveSettings = async () => {
    try {
      // TODO: Save settings to backend
      console.log('Saving settings:', { cameraSettings, detectionSettings })
    } catch (error) {
      console.error('Error saving settings:', error)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Settings</h2>
        <button
          onClick={handleSaveSettings}
          className="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring bg-primary text-primary-foreground shadow hover:bg-primary/90 h-9 px-4 py-2"
        >
          Save Changes
        </button>
      </div>

      <div className="grid gap-6">
        {/* Camera Settings */}
        <div className="rounded-lg border bg-card text-card-foreground shadow-sm">
          <div className="p-6">
            <h3 className="text-lg font-medium mb-4">Camera Settings</h3>
            <div className="space-y-4">
              <div className="grid gap-2">
                <label className="text-sm font-medium" htmlFor="resolution">
                  Resolution
                </label>
                <select
                  id="resolution"
                  value={cameraSettings.resolution}
                  onChange={(e) => setCameraSettings({
                    ...cameraSettings,
                    resolution: e.target.value
                  })}
                  className="rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                >
                  <option value="640x480">640x480</option>
                  <option value="1280x720">1280x720 (HD)</option>
                  <option value="1920x1080">1920x1080 (Full HD)</option>
                </select>
              </div>

              <div className="grid gap-2">
                <label className="text-sm font-medium" htmlFor="framerate">
                  Frame Rate
                </label>
                <input
                  id="framerate"
                  type="number"
                  min="1"
                  max="60"
                  value={cameraSettings.framerate}
                  onChange={(e) => setCameraSettings({
                    ...cameraSettings,
                    framerate: parseInt(e.target.value)
                  })}
                  className="rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Detection Settings */}
        <div className="rounded-lg border bg-card text-card-foreground shadow-sm">
          <div className="p-6">
            <h3 className="text-lg font-medium mb-4">Detection Settings</h3>
            <div className="space-y-4">
              <div className="grid gap-2">
                <label className="text-sm font-medium" htmlFor="confidence">
                  Confidence Threshold
                </label>
                <input
                  id="confidence"
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={detectionSettings.confidenceThreshold}
                  onChange={(e) => setDetectionSettings({
                    ...detectionSettings,
                    confidenceThreshold: parseFloat(e.target.value)
                  })}
                  className="w-full"
                />
                <span className="text-sm text-muted-foreground">
                  {(detectionSettings.confidenceThreshold * 100).toFixed(0)}%
                </span>
              </div>

              <div className="grid gap-2">
                <label className="text-sm font-medium" htmlFor="minSize">
                  Minimum Detection Size (px)
                </label>
                <input
                  id="minSize"
                  type="number"
                  min="1"
                  max="1000"
                  value={detectionSettings.minDetectionSize}
                  onChange={(e) => setDetectionSettings({
                    ...detectionSettings,
                    minDetectionSize: parseInt(e.target.value)
                  })}
                  className="rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                />
              </div>

              <div className="grid gap-2">
                <label className="text-sm font-medium" htmlFor="maxSize">
                  Maximum Detection Size (px)
                </label>
                <input
                  id="maxSize"
                  type="number"
                  min="1"
                  max="1000"
                  value={detectionSettings.maxDetectionSize}
                  onChange={(e) => setDetectionSettings({
                    ...detectionSettings,
                    maxDetectionSize: parseInt(e.target.value)
                  })}
                  className="rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                />
              </div>

              <div className="grid gap-2">
                <label className="text-sm font-medium" htmlFor="interval">
                  Processing Interval (ms)
                </label>
                <input
                  id="interval"
                  type="number"
                  min="50"
                  max="1000"
                  step="50"
                  value={detectionSettings.processingInterval}
                  onChange={(e) => setDetectionSettings({
                    ...detectionSettings,
                    processingInterval: parseInt(e.target.value)
                  })}
                  className="rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 