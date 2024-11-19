from fastapi.security import APIKeyHeader

access_token = 'Тут надо передавать токен доступа, access_token выдающийся при логине'
refresh_token = 'Тут надо передавать токен доступа, refresh_token выдающийся при логине'
enter_token = 'Тут надо передавать токен доступа, enter_token выдающийся admin'

api_key_header = APIKeyHeader(name="Authorization")
