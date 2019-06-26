c.ServerProxy.servers = {
    #'pyhttp': {
    #    'command': ['python', '-m', 'http.server', '{port}']
    #},
    'mongo': {
        'port': 8081,
        'absolute_url': True,
        'command': ['/home/jovyan/start_mongo.sh']
    },
    'fireworks': {
        'port': 5000,
        'command': ['lpad', '-l', '/home/jovyan/work/mp_workshop/fireworks_config/my_launchpad.yaml', 'webgui', '-s']
    }
}
