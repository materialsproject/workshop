import os

c.ServerProxy.servers = {
    'fireworks': {
        'port': 5000,
        'absolute_url': True,
        'command': [os.path.join(os.environ['HOME'], 'start_fw.sh')]
    },
}

c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.allow_remote_access = True
