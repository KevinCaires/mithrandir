import datetime
import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from jobs.models import Job
from mithrandir.tools import get_object_id
from service_orders.models import ServiceOrder


class ServiceOrderFilter(django_filters.FilterSet):
    class Meta:
        model = ServiceOrder
        fields = ['id', 'title', 'open_date', 'close_date']


class ServiceOrderNode(DjangoObjectType):
    class Meta:
        model = ServiceOrder
        interfaces = (graphene.relay.Node, )


###########################################################################
#  ______     __  __     ______     ______     __     ______     ______   # 
# /\  __ \   /\ \/\ \   /\  ___\   /\  == \   /\ \   /\  ___\   /\  ___\  # 
# \ \ \/\_\  \ \ \_\ \  \ \  __\   \ \  __<   \ \ \  \ \  __\   \ \___  \ # 
#  \ \___\_\  \ \_____\  \ \_____\  \ \_\ \_\  \ \_\  \ \_____\  \/\_____\#
#   \/___/_/   \/_____/   \/_____/   \/_/ /_/   \/_/   \/_____/   \/_____/#
###########################################################################

class Query(graphene.ObjectType):
    service_order = DjangoFilterConnectionField(
        ServiceOrderNode,
        filterset_class=ServiceOrderFilter
    )


################################################################################################
#  __    __     __  __     ______   ______     ______   __     ______     __   __     ______   # 
# /\ "-./  \   /\ \/\ \   /\__  _\ /\  __ \   /\__  _\ /\ \   /\  __ \   /\ "-.\ \   /\  ___\  # 
# \ \ \-./\ \  \ \ \_\ \  \/_/\ \/ \ \  __ \  \/_/\ \/ \ \ \  \ \ \/\ \  \ \ \-.  \  \ \___  \ # 
#  \ \_\ \ \_\  \ \_____\    \ \_\  \ \_\ \_\    \ \_\  \ \_\  \ \_____\  \ \_\\"\_\  \/\_____\# 
#   \/_/  \/_/   \/_____/     \/_/   \/_/\/_/     \/_/   \/_/   \/_____/   \/_/ \/_/   \/_____/# 
################################################################################################

class CreateServiceOrder(graphene.relay.ClientIDMutation):
    service_order = graphene.Field(ServiceOrderNode)

    class Input:
        title = graphene.String(
            description='Title of Service Order!',
            required=True,
        )
        description = graphene.String(
            description='Description of problem!',
            required=True,
        )
        per_meter = graphene.Boolean(
            description='''Your problem can be solved with mathematical measures.
            E.g. apartment painting!''',
            required=True,
        )
        job_id = graphene.String(
            description='Job Id',
            required=True,
        )
    
    def mutate_and_get_payload(root, info, **_input):  # pylint: disable=no-self-argument
        _id = _input.get('job_id')
        if not _id:
            raise Exception('Job id is required!')
        
        job_id = get_object_id(_id, 'JobNode')

        try:
            job = Job.objects.get(pk=job_id)  # pylint: disable=no-member
        except:
            raise Exception('Job id not found')
        

        service_order = ServiceOrder(
            title=_input.get('title'),
            description=_input.get('description'),
            per_meter=_input.get('per_meter'),
            job_id=job,
        )
        service_order.save()

        return CreateServiceOrder(service_order=service_order)


class UpdateServiceOrder(graphene.relay.ClientIDMutation):
    service_order = graphene.Field(ServiceOrderNode)

    class Input:
        id = graphene.String(
            description='Service Order Id',
            required=True,
        )
        title = graphene.String(
            description='Service Order Title',
        )
        service_value = graphene.Float(
            description='Valor to be payd'
        )
        description = graphene.String(
            description='Service description',
        )
        job_id = graphene.String(
            description='Job Id',            
        )

    def mutate_and_get_payload(root, info, **_input):  # pylint: disable=no-self-argument
        _id = get_object_id(_input.get('id'), 'ServiceOrderNode')

        if not _id:
            raise Exception('Service id is required!')

        #  /\_/\
        # ( o.o )
        #  > ^ <
        # Vá com calma, o código a baixo possuí gatos.

        # Pega os dados já pertencentes ao objeto. Issue #4.
        service_orders = ServiceOrder.objects.get(pk=_id)  # pylint: disable=no-member
        close_date = ''
        service_value = _input.get('service_value')

        if service_value:
            close_date = datetime.datetime.now()
        else:
            close_date = None

        data_open = service_orders.open_date

        title = _input.get( 'title')

        if not title:
            title = service_orders.title

        description = _input.get('description')

        if not description:
            description = service_orders.description

        job = ''

        if not _input.get('job_id'):
            job = Job.objects.get(pk=service_orders.job_id)  # pylint: disable=no-member
        else:
            job = Job.objects.get(pk=get_object_id(_input.get('job_id'), 'JobNode'))  # pylint: disable=no-member

        service_order = ServiceOrder(
            id=_id,
            title=title,
            service_value=_input.get('service_value'),
            close_date=close_date,
            open_date=data_open,
            description=description,
            job_id=job,
        )
        service_order.save()

        return UpdateServiceOrder(service_order=service_order)

class Mutation(graphene.AbstractType):
    create_service_order = CreateServiceOrder.Field()
    update_service_order = UpdateServiceOrder.Field()
