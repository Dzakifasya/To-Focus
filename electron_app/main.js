const { app, BrowserWindow } = require('electron')
const { spawn } = require('child_process')
const path = require('path')
const http = require('http')

let mainWindow
let djangoProcess

function waitForServer(url, callback) {
  const check = () => {
    http.get(url, () => callback()).on('error', () => {
      setTimeout(check, 500)
    })
  }
  check()
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    show: false
  })

  waitForServer('http://127.0.0.1:8000/todolist/', () => {
    mainWindow.loadURL('http://127.0.0.1:8000/todolist/')
    mainWindow.show()
  })
}

app.whenReady().then(() => {
  const djangoExe = path.join(process.resourcesPath, 'backend', 'run_django.exe')

  djangoProcess = spawn(djangoExe, [], {
    windowsHide: true
  })

  createWindow()
})

app.on('will-quit', () => {
  if (djangoProcess) djangoProcess.kill()
})
