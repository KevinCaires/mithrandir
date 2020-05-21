import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from jobs.models import Job, JobGroup, PersonalProtectiveEquipment, JobEquipment
from login.models import User
from profiles.models import UserProfile
from utils.tools import get_object_id, logged_in

class PofileNode(DjangoObjectType):
    class Meta:
        model = UserProfile
        interfaces = (graphene.relay.Node, )


class ProfileFilter(django_filters.FilterSet):
    class Meta:
        model = UserProfile
        fields = ['user']

################################################################################################
#  __    __     __  __     ______   ______     ______   __     ______     __   __     ______   # 
# /\ "-./  \   /\ \/\ \   /\__  _\ /\  __ \   /\__  _\ /\ \   /\  __ \   /\ "-.\ \   /\  ___\  # 
# \ \ \-./\ \  \ \ \_\ \  \/_/\ \/ \ \  __ \  \/_/\ \/ \ \ \  \ \ \/\ \  \ \ \-.  \  \ \___  \ # 
#  \ \_\ \ \_\  \ \_____\    \ \_\  \ \_\ \_\    \ \_\  \ \_\  \ \_____\  \ \_\\"\_\  \/\_____\# 
#   \/_/  \/_/   \/_____/     \/_/   \/_/\/_/     \/_/   \/_/   \/_____/   \/_/ \/_/   \/_____/# 
################################################################################################


class CreateProfile(graphene.relay.ClientIDMutation):
    profile = graphene.Field(UserProfile)

    class Input:

        name = graphene.String(
            description='First name.',
            required=True,
        )
        last_name = graphene.String(
            description='Last name.',
            required=True,
        )
        birth_date = graphene.Date(
            description='Birth date.',
            required=True,
        )
        phone_ddi_1 = graphene.String(
            description='Local DDI number',
            required=True,
        )
        phone_number_1 = graphene.String(
            description='Phone number.',
            required=True,
        )
        phone_ddi_2 = graphene.String(
            description='Local DDI number.'
        )
        phone_number_2 = graphene.String(
            description='Phone number.',
        )
        user = graphene.String(
            description='User id.',
            required=True,
        )
        jobs = graphene.String(
            description='Job id.'
        )
    
    @logged_in
    def mutate_and_get_payload(self, info, **_input):
        first_name = _input.get('first_name')
        last_name = _input.get('last_name')
        birth_date = _input.get('birth_date')
        phone_ddi_1 = _input.get('phone_ddi_1')
        phone_number_1 = _input.get('phone_number_1')
        user = get_object_id(_input.get('user'), 'UserNode')
        jobs = get_object_id(_input.get('jobs'), 'JobNode')

        if not first_name:
            raise Exception('First name is required!')

        if not last_name:
            raise Exception('Last name is required!')

        if not birth_date:
            raise Exception('Birth date is required!')

        if not phone_ddi_1:
            raise Exception('Phone DDI number is required!')

        if not phone_number_1:
            raise Exception('Phone number is required!')

        if not user:
            raise Exception('User id id required!')

        try:
            worker = User.objects.get(pk=user)

            if worker.worker and not jobs:
                raise Exception('Job id is required!')
        except:
            pass

        profile = UserProfile(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            phone_ddi_1=phone_ddi_1,
            phone_number_1=phone_number_1,
            phone_ddi_2=_input.get('phone_ddi_2'),
            phone_number_2=_input.get('phone_number_2'),
            user=user,
            jobs=jobs,
        )
        profile.save()

        return UserProfile(profile=profile)


class Mutation(graphene.AbstractType):
    create_user_profile = CreateProfile.Field()
