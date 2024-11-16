from settings import settings
from app.__init__ import app

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=settings.APP_PORT)