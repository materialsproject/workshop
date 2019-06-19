c.ServerProxy.servers = {
    'pyhttp': {
        'command': ['python', '-m', 'http.server', '{port}']
    },
    'mongo': {
        'port': 27017,
        'command': ['mongod', '--dbpath=/home/jovyan/mongodb']
    }
}
