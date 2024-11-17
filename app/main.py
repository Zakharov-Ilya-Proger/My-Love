from fastapi import APIRouter

main_router = APIRouter()


@main_router.get('/')
def index():
    return {'message': 'Welcome to the main page!'}
