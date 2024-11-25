import os
from app.__init__ import app
from settings import settings
import uvicorn

if __name__ == "__main__":
    os.system("python docs\\generate_docs.py")
    uvicorn.run(app, host='0.0.0.0', port=settings.APP_PORT, proxy_headers=True)
