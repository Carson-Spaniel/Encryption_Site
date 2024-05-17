const { app, BrowserWindow, Menu } = require('electron');
const { spawn } = require('child_process');

let mainWindow;
let splash;

function createWindow() {
  // Create the main window
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    // show: false, // Don't show the main window until it's ready
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  mainWindow.loadURL('http://localhost:8000');

  // Handle allowed navigation
  const allowedEndpoints = [
    'http://localhost:8000/',
    'http://localhost:8000/encrypt',
    'http://localhost:8000/decrypt',
  ];
  
  mainWindow.webContents.on('will-navigate', (event, url) => {
    const isAllowed = allowedEndpoints.some(endpoint => url.startsWith(endpoint));
    if (!isAllowed) {
      event.preventDefault();
    }
  });

  // // Disable DevTools
  // mainWindow.webContents.on('devtools-opened', () => {
  //   mainWindow.webContents.closeDevTools();
  // });

  // Remove the application menu
  Menu.setApplicationMenu(null);

  // Show the main window once it's ready
  mainWindow.once('ready-to-show', () => {
    splash.close();
    mainWindow.show();
  });
}

function createSplash() {
  splash = new BrowserWindow({
    width: 300,
    height: 200,
    frame: false,
    alwaysOnTop: true,
    transparent: true,
    webPreferences: {
      nodeIntegration: true,
    },
  });

  splash.loadFile('splash.html');
}

app.on('ready', () => {
  createSplash();
  createWindow();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
