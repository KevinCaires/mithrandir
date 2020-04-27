import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from jobs.models import Job
from service_orders.models import ServiceOrder
import datetime

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
        job_id = graphene.ID(
            description='Job Id',
            required=True,
        )
    
    def mutate_and_get_payload(root, info, **_input):  # pylint: disable=no-self-argument
        _id = _input.get('job_id')
        if not _id:
            raise Exception('Job id is required!')
        
        try:
            job = Job.objects.get(pk=_id)  # pylint: disable=no-member
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
        id = graphene.ID(
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
        job_id = graphene.ID(
            description='Job Id',            
        )

    def mutate_and_get_payload(root, info, **_input):  # pylint: disable=no-self-argument
        _id = _input.get('id')

        if not _id:
            raise Exception('Service id is required!')

        #  /\_/\
        # ( o.o )
        #  > ^ <
        # Vá com calma, a parte a baixo possuí gatos.

        close_date = ''

        if _input.get('service_value'):
            close_date = datetime.datetime.now()

        # Pega os dados já pertencentes ao objeto. Issue #4.
        # Gambiarra mode:On.
        service_orders = ServiceOrder.objects.get(pk=_id)  # pylint: disable=no-member
        data_open = service_orders.open_date

        title = _input.get( 'title')

        if not title:
            title = service_orders.title

        description = _input.get('description')

        if not description:
            description = service_orders.description

        job_id = _input.get('job_id')

        if not job_id:
            job_id = service_orders.job_id


        service_order = ServiceOrder(
            id=_input.get('id'),
            title=title,
            service_value=_input.get('service_value'),
            close_date=close_date,
            open_date=data_open,
            description=description,
        )
        service_order.save()

        return UpdateServiceOrder(service_order=service_order)

class Mutation(graphene.AbstractType):
    create_service_order = CreateServiceOrder.Field()
    update_service_order = UpdateServiceOrder.Field()
