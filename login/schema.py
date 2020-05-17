import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from itertools import chain
from login.models import User
from utils.tools import token_gen, logged_in, get_object_id

class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node, )
    
    def resolve_all_permissions(self, info, **kwargs):
        user = info.context.user
        user_permissions = user.user_psermissions.all()
        group_permissions = [g.group_permissions.all() for g in user.groups.all()]
        response = set(chain(user_permissions, *group_permissions))

        return [p.codename for p in response]


###########################################################################
#  ______     __  __     ______     ______     __     ______     ______   # 
# /\  __ \   /\ \/\ \   /\  ___\   /\  == \   /\ \   /\  ___\   /\  ___\  # 
# \ \ \/\_\  \ \ \_\ \  \ \  __\   \ \  __<   \ \ \  \ \  __\   \ \___  \ # 
#  \ \___\_\  \ \_____\  \ \_____\  \ \_\ \_\  \ \_\  \ \_____\  \/\_____\#
#   \/___/_/   \/_____/   \/_____/   \/_/ /_/   \/_/   \/_____/   \/_____/#
###########################################################################

class Query(graphene.ObjectType):
    login = graphene.List(UserNode)

    def resolve_login(self, info, **kwargs):
        return User.objects.all()



################################################################################################
#  __    __     __  __     ______   ______     ______   __     ______     __   __     ______   # 
# /\ "-./  \   /\ \/\ \   /\__  _\ /\  __ \   /\__  _\ /\ \   /\  __ \   /\ "-.\ \   /\  ___\  # 
# \ \ \-./\ \  \ \ \_\ \  \/_/\ \/ \ \  __ \  \/_/\ \/ \ \ \  \ \ \/\ \  \ \ \-.  \  \ \___  \ # 
#  \ \_\ \ \_\  \ \_____\    \ \_\  \ \_\ \_\    \ \_\  \ \_\  \ \_____\  \ \_\\"\_\  \/\_____\# 
#   \/_/  \/_/   \/_____/     \/_/   \/_/\/_/     \/_/   \/_/   \/_____/   \/_/ \/_/   \/_____/# 
################################################################################################

class LoginCreate(graphene.relay.ClientIDMutation):
    """
    Cria um login.
    """
    user = graphene.Field(UserNode)

    class Input:
        username = graphene.String(
            description='Login name',
            required=True,
        )
        email = graphene.String(
            description='Email',
            required=True,
        )
        password = graphene.String(
            description='Minimum six chars, maximum fifty. Please include symbols and numbers.',
            required=True,
        )
        cpf = graphene.String(
            description='Document number.',
            required=True,
        )
    
    def mutate_and_get_payload(self, info, **_input):
        cpf = _input.get('cpf')
        
        if len(cpf) < 11 or len(cpf) > 14:
            raise Exception('Invalid document!')

        user = User(
            username=_input.get('username'),
            email=_input.get('email'),
            cpf=cpf,
        )
        user.set_password(_input.get('password'))
        user.save()

        return LoginCreate(user=user)


class Login(graphene.relay.ClientIDMutation):
    login = graphene.Field(UserNode)

    class Input:
        email = graphene.String(
            required=True,
            description='Email.',
        )
        password = graphene.String(
            required=True,
            description='Password.'
        )
    
    def mutate_and_get_payload(self, info, **_input):
        user = User.objects.get(email=_input.get('email'))
        login = ''
        if user.check_password(_input.get('password')):
            token = token_gen(user.id)

            login = User(token=token)
            login.save()

        return Login(login=login)


class Mutation(graphene.AbstractType):
    create_login = LoginCreate.Field()
    login = Login.Field()
