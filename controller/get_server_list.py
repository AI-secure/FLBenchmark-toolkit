import os
import json

host_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwcml2aWxlZ2UiOiJob3N0IiwidXNlcl9pZCI6IjAzYmJjZjE5MTI1MDNkMzMzM2NmODBjZjEwMTNhZDg0NmI2MzRkMTk5NmMzMzY3ODZkZGYxYTU2OTg3NjQzNDIzMCIsImV4cCI6MTcxODIwOTM0Nn0.NZoUVyWzd_O_HGaYevTsyyTsSqusDSYoeJhzkwdP6KM"
servers = os.listdir("servers")
server_list={}
id=0
for server in servers:
    if not server.startswith('.'):
        server_list["test-{}".format(id)]=["http://{}:80".format(server),host_token]
        id+=1

with open('server_list.json', 'w') as outfile:
    json.dump(server_list, outfile)
