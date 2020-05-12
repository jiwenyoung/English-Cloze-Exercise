const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require("path")

const ENV = 'development'  //options: development / production
let server

const createWindow = () => {
    // Create the browser window.
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        }
    })

    //remove menu bar
    if(ENV === 'production'){
        win.removeMenu()
    }

    // and load the index.html of the app.
    win.loadFile('gui/index.html',{ "query": { "env" : ENV } })

    // Open the DevTools.
    if(ENV === 'development'){
        win.webContents.openDevTools()
    }
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.

app.on("ready", () => {
    if(ENV === 'development'){
        process.chdir("cli")
        command = ""
        if(process.platform === 'linux'){
            command = "python3"
        }else if(process.platform === 'win32'){
            command = "python.exe"
        }
        server = spawn(command,["cloze.py", "gui"])
    }else if(ENV === 'production'){
        let file = ''
        if(process.platform === 'linux'){
            file = 'cloze'
        }else if(process.platform === 'win32'){
            file = 'cloze.exe'
        }
        const backendpath = path.join(__dirname,"cloze") 
        const backend = path.join(__dirname,"cloze",file)
        process.chdir(backendpath)
        server = spawn(backend, ["gui"])
    }
    app.whenReady().then(createWindow)
    server.stderr.on("data", (error) => {
        console.error(error.toString("utf-8"))
        app.quit()
    })
})


// Quit when all windows are closed.
app.on('window-all-closed', () => {
    server.kill()
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

