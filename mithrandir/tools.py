from base64 import b64decode, b64encode
from blacklist.models import TokenList
from graphql_relay import from_global_id
from functools import wraps

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
id

def logged_in(function):
    '''
    JTW Authorization token 
    '''
    @wraps(function)
    def decorated(*args, **kwargs):
        token = args[1].context.META.get('HTTP_AUTHORIZATION')
        black_listed = TokenList.objects.filter(token=token)  # pylint: disable=no-member
        
        if black_listed:
            raise Exception('Session Expired, please log in again!')

        user = args[1].context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return function(*args, **kwargs)
    return decorated
