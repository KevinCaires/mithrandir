from decouple import config
from functools import wraps
from graphql_relay import from_global_id
import jwt
from login.models import User
from time import time

SECRET_KEY = config('SECRET_KEY')

def get_object_id(hash_id, object_name):
    """
    Valida um id recebido em b64 e se é equivalente ao objeto esperado.
    """
    if not hash_id:
        return ''
    
    try:
        object_type, object_id = from_global_id(hash_id)
    except:
        raise Exception('Invalid data!')

    if object_type != object_name:
        raise Exception('Invalid Id!')

    return int(object_id)


def logged_in(function):
    '''
    Valida um token JTW.
    '''
    @wraps(function)
    def decorated(*args, **kwargs):
        token = args[1].context.META.get('HTTP_AUTHORIZATION')

        try:
            user = jwt.decode(token, SECRET_KEY, algorithm='HS256')
        
        except jwt.ExpiredSignatureError:
            raise Exception('Token is not valid token!')

        except jwt.DecodeError:
            raise Exception('Invalid token')

        if user.get('is_anonymous'):
            raise Exception('Not logged in!')

        return function(*args, **kwargs)
    return decorated


def token_gen(user_id):
    """
    Gera uma token JWT.
    """
    try:
        user = User.objects.get(pk=user_id)
        payload = {
            'uid':user.id,
            'username':user.username,
            'email':user.email,
            'cpf':user.cpf,
            'worker':user.worker,
            'is_anonymous':False,
            'exp':int(time()) + 3600,
        }
    
    except Exception as ex:
        print(f'''
        
        ERROR: {ex}
        
        ''')
        payload = {
            'uid':None,
            'username':None,
            'email':None,
            'cpf':None,
            'worker':None,
            'is_anonymous':True,
            'exp':int(time()) + 1,
        }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

    return token
