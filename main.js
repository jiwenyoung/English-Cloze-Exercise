const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');

let server

function createWindow() {
    // Create the browser window.
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        }
    })

    // and load the index.html of the app.
    win.loadFile('gui/index.html')

    // Open the DevTools.
    win.webContents.openDevTools()

    //Send data to render process
    win.webContents.on('did-finish-load', () => {
        win.webContents.send('ping', 'whoooooooh!');
    })
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.

app.whenReady().then(createWindow)
app.on("ready", () => {
    process.chdir("./cli")
    //server = spawn("python3", ["main.py", "gui"])
    //setTimeout(() => {
    //}, 1000);
})


// Quit when all windows are closed.
app.on('window-all-closed', () => {
    //server.kill("SIGHUP")

    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow()
    }
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.

