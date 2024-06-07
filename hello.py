#!/usr/bin/env python
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
  version = os.environ.get('VERSION', 'unknown')
  return f'Hello World version {version}!'

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 8080))
  app.run(host='0.0.0.0', port=port)