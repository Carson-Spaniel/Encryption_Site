const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  mainWindow.loadURL('http://localhost:8000');

  const allowedEndpoints = [
    'http://localhost:8000/',
    // 'http://localhost:8000/login',
    // 'http://localhost:8000/signup',
    'http://localhost:8000/encrypt',
    'http://localhost:8000/decrypt',
  ];
  
  mainWindow.webContents.on('will-navigate', (event, url) => {
    // Check if the URL matches any of the allowed endpoints
    const isAllowed = allowedEndpoints.some(endpoint => url.startsWith(endpoint));
    
    // If the URL is not in the list of allowed endpoints, prevent navigation
    if (!isAllowed) {
      event.preventDefault();
    }
  });

  // Disable DevTools
  mainWindow.webContents.on('devtools-opened', () => {
    mainWindow.webContents.closeDevTools();
  });
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    const serverProcess = spawn('taskkill', ['/f', '/im', 'python.exe', '/t']);
    serverProcess.on('close', () => {
      console.log('Django server closed.');
    });
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// // Ensure that the Django server is closed when Electron exits
// app.on('will-quit', () => {
//   const serverProcess = spawn('taskkill', ['/f', '/im', 'python.exe', '/t']);
//   serverProcess.on('close', () => {
//     console.log('Django server closed.');
//   });
// });
