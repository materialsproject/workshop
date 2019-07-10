c.ServerProxy.servers = {
    'pyhttp': {
        'command': ['python', '-m', 'http.server', '{port}']
    },
    'mongo': {
        'port': 8081,
        'absolute_url': True,
        'command': ['/home/jovyan/start_mongo.sh']
    },
    'fireworks': {
        'port': 5000,
        'absolute_url': True,
        'command': ['/home/jovyan/start_fw.sh']
    }
}
