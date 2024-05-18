const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
  // Create the main window
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    minWidth: 650,
    minHeight: 600,
    show: false, // Don't show the main window until it's ready
    icon: path.join(__dirname, 'company_images/secureit.png'),
    webPreferences: {
      sandbox: true,
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
  // Menu.setApplicationMenu(null);

  // Show the main window once it's ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });
}

app.on('ready', () => {
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

app.on('browser-window-blur', () => {
  if (mainWindow) {
    mainWindow.webContents.insertCSS(`
      body {
        filter: blur(10px);
      }
    `);
  }
});

app.on('browser-window-focus', () => {
  if (mainWindow) {
    mainWindow.webContents.insertCSS(`
      body {
        filter: blur(0px);
      }
    `);
  }
});
