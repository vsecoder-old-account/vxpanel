#!/usr/bin/python
import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.responses import Response

import os
import psutil
import datetime
import platform
import contextlib
import time
import socket
#import speedtest

# Create server
app = FastAPI()
templates = Jinja2Templates('templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

def stat():
    mem = psutil.virtual_memory()
    active_since = datetime.datetime.fromtimestamp(psutil.boot_time())
    cpu = psutil.cpu_percent()
    internet = psutil.net_io_counters()
    #st = speedtest.Speedtest()

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
        'ip': socket.gethostbyname(socket.getfqdn()),
        'uptime': datetime.datetime.now() - active_since,
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'cpu': {
            'used': psutil.cpu_count() / 100 * cpu,
            'free': psutil.cpu_count() - psutil.cpu_count() / 100 * cpu,
            'percent': cpu
        },
        'memory': {
            'total': round(mem.total / 1024 / 1024),
            'avaliable': round(mem.available / 1024 / 1024),
            'used': round(mem.used / 1024 / 1024),
            'free': round(mem.free / 1024 / 1024),
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
        },
        'internet': {
            #'upload': st.upload(),
            #'donwload': st.donwload(),
            #'ping': st.ping(),
            'bytes_sent': internet.bytes_sent,
            'bytes_recv': internet.bytes_recv,
            'packets_sent': internet.packets_sent,
            'packets_recv': internet.packets_recv,
            'errin': internet.errin,
            'errout': internet.errout,
            'dropin': internet.dropin,
            'dropout': internet.dropout
        }
    }
    return data

def test():
    with open("test.txt", 'a') as fout, contextlib.redirect_stdout(fout):
        psutil.test()
    f = open("test.txt", 'r')
    test = f.read()
    f.close()
    os.remove("test.txt")
    return test

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
    return templates.TemplateResponse('logs.html', {'request': request, 'data': test()})

@app.get('/settings')
def panel_page(request: Request):
    return 'In dev'

@app.get('/ssh')
def panel_page(request: Request):
    return 'In dev'

@app.get('/api')
def panel_page(request: Request):
    return stat()

@app.get('/test')
def panel_page(request: Request):
    return test()

# Start server
if __name__ == "__main__":
    # dev
    uvicorn.run('app:app',
        host="0.0.0.0", 
        port=int(os.environ.get('PORT', False)),
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