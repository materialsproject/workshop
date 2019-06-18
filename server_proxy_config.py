c.ServerProxy.servers = {
    'pyhttp': {
        'command': ['python', '-m', 'http.server', '{port}']
    },
    'mongo': {
        'command': ['mongod'],
        'port': 27017,
        'enabled': False
    }
}
