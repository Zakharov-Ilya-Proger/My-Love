from settings import settings
from app.__init__ import app
import subprocess

if __name__ == '__main__':
    subprocess.run(['python', 'docs\\generate_docs.py'])
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=settings.APP_PORT)