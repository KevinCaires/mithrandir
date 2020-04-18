from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

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

    # Classe de teste para o login.
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Log in to continue!')

        return user


################################################################################################
#  __    __     __  __     ______   ______     ______   __     ______     __   __     ______   # 
# /\ "-./  \   /\ \/\ \   /\__  _\ /\  __ \   /\__  _\ /\ \   /\  __ \   /\ "-.\ \   /\  ___\  # 
# \ \ \-./\ \  \ \ \_\ \  \/_/\ \/ \ \  __ \  \/_/\ \/ \ \ \  \ \ \/\ \  \ \ \-.  \  \ \___  \ # 
#  \ \_\ \ \_\  \ \_____\    \ \_\  \ \_\ \_\    \ \_\  \ \_\  \ \_____\  \ \_\\"\_\  \/\_____\# 
#   \/_/  \/_/   \/_____/     \/_/   \/_/\/_/     \/_/   \/_/   \/_____/   \/_/ \/_/   \/_____/# 
################################################################################################

class CreateUser(graphene.Mutation):
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

    def mutate(self, info, **_input):
        user = get_user_model()(
            username=_input.get('username'),
            email=_input.get('email'),
            first_name=_input.get('first_name'),
            last_name=_input.get('last_name'),
        )
        user.save()
        user.set_password(_input.get('password'))

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
