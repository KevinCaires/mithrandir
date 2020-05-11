from django.contrib.auth import get_user_model
import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mithrandir.tools import logged_in
class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class UserNode(DjangoObjectType):
    class Meta:
        model = get_user_model()
        interfaces = (graphene.relay.Node,)

###########################################################################
#  ______     __  __     ______     ______     __     ______     ______   # 
# /\  __ \   /\ \/\ \   /\  ___\   /\  == \   /\ \   /\  ___\   /\  ___\  # 
# \ \ \/\_\  \ \ \_\ \  \ \  __\   \ \  __<   \ \ \  \ \  __\   \ \___  \ # 
#  \ \___\_\  \ \_____\  \ \_____\  \ \_\ \_\  \ \_\  \ \_____\  \/\_____\#
#   \/___/_/   \/_____/   \/_____/   \/_/ /_/   \/_/   \/_____/   \/_____/#
###########################################################################

class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    @logged_in
    def resolve_me(self, info):
        """
        Teste function
        """
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Log in to continue!')

        return get_user_model().objects.all()




################################################################################################
#  __    __     __  __     ______   ______     ______   __     ______     __   __     ______   # 
# /\ "-./  \   /\ \/\ \   /\__  _\ /\  __ \   /\__  _\ /\ \   /\  __ \   /\ "-.\ \   /\  ___\  # 
# \ \ \-./\ \  \ \ \_\ \  \/_/\ \/ \ \  __ \  \/_/\ \/ \ \ \  \ \ \/\ \  \ \ \-.  \  \ \___  \ # 
#  \ \_\ \ \_\  \ \_____\    \ \_\  \ \_\ \_\    \ \_\  \ \_\  \ \_____\  \ \_\\"\_\  \/\_____\# 
#   \/_/  \/_/   \/_____/     \/_/   \/_/\/_/     \/_/   \/_/   \/_____/   \/_/ \/_/   \/_____/# 
################################################################################################

class CreateUser(graphene.relay.ClientIDMutation):
    """ Cria um usuário """
    user = graphene.Field(UserType)

    class Input:
        username = graphene.String(
            description='Login name',
            required=True,
        )
        first_name = graphene.String(description='First name')
        last_name = graphene.String(description='Last name')
        email = graphene.String(
            description='Login email',
            required=True,
        )
        password = graphene.String(
            description='Password. Recommended letters, numbers and special chars',
            required=True,
        )

    def mutate_and_get_payload(self, info, **_input):
        user = get_user_model()(
            username=_input.get('username'),
            email=_input.get('email'),
            first_name=_input.get('first_name'),
            last_name=_input.get('last_name'),
        )
        user.set_password(_input.get('password'))
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.AbstractType):
    create_user = CreateUser.Field()
