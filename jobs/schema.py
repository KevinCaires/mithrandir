import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from jobs.models import Job

class JobFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = ['name', 'per_meter', 'job_group']


class JobNode(DjangoObjectType):
    class Meta:
        model = Job
        interfaces = (graphene.relay.Node, )


###########################################################################
#  ______     __  __     ______     ______     __     ______     ______   # 
# /\  __ \   /\ \/\ \   /\  ___\   /\  == \   /\ \   /\  ___\   /\  ___\  # 
# \ \ \/\_\  \ \ \_\ \  \ \  __\   \ \  __<   \ \ \  \ \  __\   \ \___  \ # 
#  \ \___\_\  \ \_____\  \ \_____\  \ \_\ \_\  \ \_\  \ \_____\  \/\_____\#
#   \/___/_/   \/_____/   \/_____/   \/_/ /_/   \/_/   \/_____/   \/_____/#
###########################################################################

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
        name = graphene.String(
            description='Name of job!',
            required=True,
        )
        per_meter = graphene.Boolean(
            description='This job can be charged per meter!',
            required=True,
        )
        value_per_meter = graphene.Float(
            description='If can be charged per meter, what is the price of the meter?'
        )
        job_group = graphene.String(
            description='Group of job',
            required=True,
        )

    def mutate_and_get_payload(root, info, **_input):  # pylint: disable=no-self-argument
        job = Job(
            name=_input.get('name'),
            per_meter=_input.get('per_meter'),
            value_per_meter=_input.get('value_per_meter'),
            job_group=_input.get('job_group'),
        )
        job.save()

        return CreateJob(job=job)


class UpdateJob(graphene.relay.ClientIDMutation):
    job = graphene.Field(JobNode)

    class Input:
        id = graphene.ID(
            descripition='Job Id',
            required=True,
        )
        name = graphene.String(
            description='Job Title'
        )
        per_meter = graphene.Boolean(
            description='This job can be charged per meter!'
        )
        value_per_meter = graphene.Float(
            description='If can be charged per meter, what is the price of the meter?'
        )
        job_group = graphene.String(
            description='Group of job'
        )
    
    def mutate_and_get_payload(root, info, **_input):  # pylint: disable=no-self-argument
        _id = _input.get('id')

        if not _id:
            raise Exception('Id is required!')
        
        per_meter = _input.get('per_meter')

        if not per_meter:
            raise Exception('Per meter is required!')

        jobs = Job.objects.get(pk=_id)  # pylint: disable=no-member
        name = _input.get('name')
        
        if not name:
            name = jobs.name
        
        value_per_meter = _input.get('value_per_meter')

        if not value_per_meter:
            value_per_meter = jobs.value_per_meter

        job_group = _input.get('job_group')

        if not job_group:
            job_group = jobs.job_group
        
        job = Job(
            id=_id,
            name=name,
            per_meter=per_meter,
            value_per_meter=value_per_meter,
            job_group=job_group,
        )
        job.save()

        return UpdateJob(job=job)


class Mutation(graphene.AbstractType):
    create_job = CreateJob.Field()
    update_job = UpdateJob.Field()
