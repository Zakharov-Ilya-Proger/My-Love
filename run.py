import os
import uvicorn
from settings import settings
from app.__init__ import app

if __name__ == '__main__':
    os.system('python docs\\generate_docs.py')
    uvicorn.run(app, host='0.0.0.0', port=settings.APP_PORT)