const { app, BrowserWindow, protocol } = require('electron')
const path = require('path')

var arguments = process.argv.slice(2)


const createWindow = () => {
    // Create the browser window.
    const WEB_FOLDER = '_templates/electron';
    const PROTOCOL = 'file';

    protocol.interceptFileProtocol(PROTOCOL, (request, callback) => {
        // Strip protocol
        let url = request.url.substr(PROTOCOL.length + 1);

        // Build complete path for node require function
        url = path.join(__dirname, WEB_FOLDER, url);

        // Replace backslashes by forward slashes (windows)
        // url = url.replace(/\\/g, '/');
        url = path.normalize(url);

        console.log(url);
        callback({ path: url });
    });

    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: false,
            // preload: path.join(__dirname, 'preload.js')
        }
    })

    if (arguments.includes('--dev')) {
        // mainWindow.loadURL('http://localhost:1234/')

        // and load the index.html of the app.
        mainWindow.loadURL('file:///index.html');
        // mainWindow.loadFile('_templates/electron/index.html')

        // Open the DevTools.
        mainWindow.webContents.openDevTools()
    }
    else
        mainWindow.loadURL('http://localhost:8000/')

}

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        app.quit();
    }
});
