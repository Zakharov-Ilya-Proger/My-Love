from fastapi import APIRouter

main = APIRouter()


@main.get('/')
def index():
    return {'message': 'Welcome to the main page!'}
