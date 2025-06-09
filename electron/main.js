const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const isDev = process.env.NODE_ENV !== 'production';

let mainWindow = null;
let retries = 0;
const maxRetries = 3;

function createWindow() {
    // Create the browser window
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js')
        },
        // Add these options for better window appearance
        backgroundColor: '#ffffff',
        show: false // Don't show until ready
    });

    // Load the app
    if (isDev) {
        loadDevelopmentApp();
    } else {
        loadProductionApp();
    }

    // Show window when ready to prevent flashing
    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
    });

    // Handle window state
    mainWindow.on('closed', function () {
        mainWindow = null;
    });
}

function loadDevelopmentApp() {
    mainWindow.loadURL('http://localhost:5173')
        .then(() => {
            mainWindow.webContents.openDevTools();
            retries = 0; // Reset retries on successful load
        })
        .catch((err) => {
            console.error('Failed to load development URL:', err);
            if (retries < maxRetries) {
                retries++;
                console.log(`Retrying... (${retries}/${maxRetries})`);
                setTimeout(loadDevelopmentApp, 1000); // Retry after 1 second
            } else {
                console.error('Max retries reached. Please ensure the Vite server is running.');
                app.quit();
            }
        });
}

function loadProductionApp() {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'))
        .catch((err) => {
            console.error('Failed to load production build:', err);
        });
}

// This method will be called when Electron has finished initialization
app.whenReady().then(() => {
    createWindow();

    app.on('activate', function () {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

// Quit when all windows are closed
app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') app.quit();
});

// Handle IPC messages
ipcMain.handle('get-app-path', () => app.getAppPath());

ipcMain.handle('get-camera-permissions', async () => {
    try {
        const { systemPreferences } = require('electron');
        const status = await systemPreferences.getMediaAccessStatus('camera');
        return status === 'granted';
    } catch (error) {
        console.error('Error checking camera permissions:', error);
        return false;
    }
});

ipcMain.handle('is-dev', () => isDev);

ipcMain.handle('get-version', () => app.getVersion());

// Camera-related handlers
ipcMain.handle('get-camera-list', async () => {
    try {
        const { desktopCapturer } = require('electron');
        const sources = await desktopCapturer.getSources({ types: ['camera'] });
        return sources.map(source => ({
            id: source.id,
            name: source.name,
            thumbnail: source.thumbnail.toDataURL()
        }));
    } catch (error) {
        console.error('Error getting camera list:', error);
        return [];
    }
});

// File system handlers
ipcMain.handle('save-inspection-data', async (event, data) => {
    try {
        const fs = require('fs').promises;
        const savePath = path.join(app.getPath('userData'), 'inspections');
        await fs.mkdir(savePath, { recursive: true });
        await fs.writeFile(
            path.join(savePath, `inspection_${Date.now()}.json`),
            JSON.stringify(data, null, 2)
        );
        return true;
    } catch (error) {
        console.error('Error saving inspection data:', error);
        return false;
    }
});

ipcMain.handle('load-inspection-data', async (event, id) => {
    try {
        const fs = require('fs').promises;
        const filePath = path.join(app.getPath('userData'), 'inspections', `inspection_${id}.json`);
        const data = await fs.readFile(filePath, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error('Error loading inspection data:', error);
        return null;
    }
});

ipcMain.handle('export-report', async (event, data) => {
    try {
        const fs = require('fs').promises;
        const exportPath = path.join(app.getPath('documents'), 'Antemortem Reports');
        await fs.mkdir(exportPath, { recursive: true });
        await fs.writeFile(
            path.join(exportPath, `report_${Date.now()}.json`),
            JSON.stringify(data, null, 2)
        );
        return true;
    } catch (error) {
        console.error('Error exporting report:', error);
        return false;
    }
}); 