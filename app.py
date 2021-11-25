#!/usr/bin/python
import uvicorn, os
from fastapi import FastAPI
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.responses import Response

import os
import json
import psutil
import datetime
import platform

# Create server
app = FastAPI()
templates = Jinja2Templates('templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

def stat():
    mem = psutil.virtual_memory()
    active_since = datetime.datetime.fromtimestamp(psutil.boot_time())
    cpu = psutil.cpu_percent()
    
    status_cpu = 'normal'
    if cpu > 70: status_cpu = 'high'
    elif cpu > 30: status_cpu = 'middle'
    else: status_cpu = 'normal'
    
    status_memory = 'normal'
    if mem.percent > 70: status_memory = 'high'
    elif mem.percent > 30: status_memory = 'middle'
    else: status_memory = 'normal'
    
    status_disk = 'normal'
    if psutil.disk_usage('/').percent > 70: status_disk = 'high'
    elif psutil.disk_usage('/').percent > 30: status_disk = 'middle'
    else: status_disk = 'normal'
    data = {
        'cpu': {
            'used': psutil.cpu_count() / 100 * cpu,
            'free': psutil.cpu_count() - psutil.cpu_count() / 100 * cpu,
            'percent': cpu
        },
        'uptime': (datetime.datetime.now() - active_since).days,
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'memory': {
            'total': round(mem.total / 1024 / 1024),
            'avaliable': round(mem.available / 1024 / 1024),
            'used':round( mem.used / 1024 / 1024),
            'free':round( mem.free / 1024 / 1024),
            'active': round(mem.active / 1024 / 1024),
            'inactive': round(mem.inactive / 1024 / 1024),
            'cached': round(mem.cached / 1024 / 1024),
            'buffers': round(mem.buffers / 1024 / 1024),
            'shared': round(mem.shared / 1024 / 1024),
            'percent': mem.percent
        },
        'disk': {
            'total': round(psutil.disk_usage('/').total / 1024 / 1024),
            'used': round(psutil.disk_usage('/').used / 1024 / 1024),
            'free': round(psutil.disk_usage('/').free / 1024 / 1024),
            'percent': psutil.disk_usage('/').percent
        },
        'status': {
            'cpu': status_cpu,
            'memory': status_memory,
            'disk': status_disk
        }
    }
    return data

# Server home page
@app.get('/')
def home_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@app.get('/page')
def panel_page(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'data': stat()})

@app.get('/info')
def panel_page(request: Request):
    return templates.TemplateResponse('info.html', {'request': request, 'data': stat()})

@app.get('/logs')
def logs_page(request: Request):
    return templates.TemplateResponse('logs.html', {'request': request})

# Start server
if __name__ == "__main__":
    # dev
    uvicorn.run('app:app',
        host="0.0.0.0", 
        port=8000,
        log_level="debug",
        http="h11",
        reload=True,
        use_colors=True,
        workers=3
    )
    # prod
    #uvicorn.run('app:app',
    #    host="0.0.0.0", 
    #    port=80,
    #    http="h11"
    #)
