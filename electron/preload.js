const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld(
    'electron',
    {
        // Basic app functionality
        getAppPath: () => ipcRenderer.invoke('get-app-path'),
        getCameraPermissions: () => ipcRenderer.invoke('get-camera-permissions'),
        
        // Event listeners
        onUpdateAvailable: (callback) => {
            const subscription = (_event, value) => callback(value);
            ipcRenderer.on('update-available', subscription);
            return () => {
                ipcRenderer.removeListener('update-available', subscription);
            };
        },
        onError: (callback) => {
            const subscription = (_event, value) => callback(value);
            ipcRenderer.on('error', subscription);
            return () => {
                ipcRenderer.removeListener('error', subscription);
            };
        },
        
        // Camera-related methods
        startCamera: (deviceId) => ipcRenderer.invoke('start-camera', deviceId),
        stopCamera: () => ipcRenderer.invoke('stop-camera'),
        getCameraList: () => ipcRenderer.invoke('get-camera-list'),
        
        // System information
        platform: process.platform,
        
        // File system operations
        saveInspectionData: (data) => ipcRenderer.invoke('save-inspection-data', data),
        loadInspectionData: (id) => ipcRenderer.invoke('load-inspection-data', id),
        exportReport: (data) => ipcRenderer.invoke('export-report', data),
        
        // Utility methods
        isDev: () => ipcRenderer.invoke('is-dev'),
        getVersion: () => ipcRenderer.invoke('get-version')
    }
); 