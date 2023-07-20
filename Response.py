import json
import os

class Response:
    
    def __init__(self, statusCode, body, headers={
                'Access-Control-Allow-Origin': os.environ['ALLOWED_ORIGINS'],
                'Content-Type': 'application/json'
            }):
        self.statusCode=statusCode
        self.body=body
        self.headers=headers
        
    def __str__(self):
        return 'Response(body={}, statusCode={}, headers={})'.format(self.body, self.statusCode, self.headers)
        