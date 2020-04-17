from base64 import b64decode
import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from service_orders.models import ServiceOrder

class ServiceOrderFilter(django_filters.FilterSet):
    class Meta:
        model = ServiceOrder
        fields = ['id', 'title', 'open_date', 'close_date']


class ServiceOrserNode(DjangoObjectType):
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
        ServiceOrserNode,
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
    service_order = graphene.Field(ServiceOrserNode)

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
        # job = graphene.ID(
        #     description='Job Id',
        #     required=True,
        # )
    
    def mutate_and_get_payload(root, info, **_input):  # pylint: disable=no-self-argument
        service_order = ServiceOrder(
            title=_input.get('title'),
            description=_input.get('description'),
            per_meter=_input.get('per_meter'),
        )
        service_order.save()

        return CreateServiceOrder(service_order=service_order)


class Mutation(graphene.AbstractType):
    create_service_order = CreateServiceOrder.Field()
