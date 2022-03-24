const { app, BrowserWindow } = require('electron')
const path = require('path')

var arguments = process.argv.slice(2)

const createWindow = () => {
    // Create the browser window.
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        // webPreferences: {
        //     preload: path.join(__dirname, 'preload.js')
        // }
    })

    // and load the index.html of the app.
    // mainWindow.loadFile('dist/index.html')
    if (arguments.includes('--dev')) {

        mainWindow.loadURL('http://localhost:1234/')
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
