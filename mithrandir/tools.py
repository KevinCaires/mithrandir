from base64 import b64decode, b64encode
from graphql_relay import from_global_id

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
