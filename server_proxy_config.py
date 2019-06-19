c.ServerProxy.servers = {
    'pyhttp': {
        'command': ['python', '-m', 'http.server', '{port}']
    },
    'mongo': {
        'command': ['mongod', '--dbpath=/home/jovyan/data'],
        'port': 27017,
        'enabled': False
    }
}
