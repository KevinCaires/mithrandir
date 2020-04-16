import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from jobs.models import Job

###########################################################################
#  ______     __  __     ______     ______     __     ______     ______   # 
# /\  __ \   /\ \/\ \   /\  ___\   /\  == \   /\ \   /\  ___\   /\  ___\  # 
# \ \ \/\_\  \ \ \_\ \  \ \  __\   \ \  __<   \ \ \  \ \  __\   \ \___  \ # 
#  \ \___\_\  \ \_____\  \ \_____\  \ \_\ \_\  \ \_\  \ \_____\  \/\_____\#
#   \/___/_/   \/_____/   \/_____/   \/_/ /_/   \/_/   \/_____/   \/_____/#
###########################################################################
class JobFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = ['name', 'per_meter', 'job_group']


class JobNode(DjangoObjectType):
    class Meta:
        model = Job
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    job = DjangoFilterConnectionField(
        JobNode,
        filterset_class=JobFilter,
    )


################################################################################################
#  __    __     __  __     ______   ______     ______   __     ______     __   __     ______   # 
# /\ "-./  \   /\ \/\ \   /\__  _\ /\  __ \   /\__  _\ /\ \   /\  __ \   /\ "-.\ \   /\  ___\  # 
# \ \ \-./\ \  \ \ \_\ \  \/_/\ \/ \ \  __ \  \/_/\ \/ \ \ \  \ \ \/\ \  \ \ \-.  \  \ \___  \ # 
#  \ \_\ \ \_\  \ \_____\    \ \_\  \ \_\ \_\    \ \_\  \ \_\  \ \_____\  \ \_\\"\_\  \/\_____\# 
#   \/_/  \/_/   \/_____/     \/_/   \/_/\/_/     \/_/   \/_/   \/_____/   \/_/ \/_/   \/_____/# 
################################################################################################

class CreateJob(graphene.relay.ClientIDMutation):
    job = graphene.Field(JobNode)

    class Input:
        name = graphene.String(required=True)
        per_meter = graphene.Boolean(required=True)
        value_per_meter = graphene.Float()
        job_group = graphene.String(required=True)

    def mutate_and_get_payload(root, info, **_input):  # pylint: disable=no-self-argument
        job = Job(
            name=_input.get('name'),
            per_meter=_input.get('per_meter'),
            value_per_meter=_input.get('value_per_meter'),
            job_group=_input.get('job_group'),
        )
        job.save()

        return CreateJob(job=job)


class Mutation(graphene.AbstractType):
    create_job = CreateJob.Field()
