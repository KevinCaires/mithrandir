import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from jobs.models import Job, JobGroup, PersonalProtectiveEquipment, JobEquipment
from utils.tools import get_object_id


class JobGroupFilter(django_filters.FilterSet):
    class Meta:
        model = JobGroup
        fields = ['name']


class PersonalProtectiveEquipmentFilter(django_filters.FilterSet):
    class Meta:
        model = PersonalProtectiveEquipment
        fields = ['name']


class JobEquipmentFilter(django_filters.FilterSet):
    class Meta:
        model = JobEquipment
        fields = ['name']

class JobFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = ['name', 'per_meter', 'job_group']

class PersonalProtectiveEquipmentNode(DjangoObjectType):
    class Meta:
        model = PersonalProtectiveEquipment
        interfaces = (graphene.relay.Node, )


class JobEquipmentNode(DjangoObjectType):
    class Meta:
        model = JobEquipment
        interfaces = (graphene.relay.Node, )


class JobNode(DjangoObjectType):
    class Meta:
        model = Job
        interfaces = (graphene.relay.Node, )


class JobGroupNode(DjangoObjectType):
    class Meta:
        model = JobGroup
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
    job_equipment = DjangoFilterConnectionField(
        JobEquipmentNode,
        filterset_class=JobEquipmentFilter,
    )
    job_group = DjangoFilterConnectionField(
        JobGroupNode,
        filterset_class=JobGroupFilter,
    )
    personal_protective_equipment = DjangoFilterConnectionField(
        PersonalProtectiveEquipmentNode,
        filterset_class=PersonalProtectiveEquipmentFilter,
    )

################################################################################################
#  __    __     __  __     ______   ______     ______   __     ______     __   __     ______   # 
# /\ "-./  \   /\ \/\ \   /\__  _\ /\  __ \   /\__  _\ /\ \   /\  __ \   /\ "-.\ \   /\  ___\  # 
# \ \ \-./\ \  \ \ \_\ \  \/_/\ \/ \ \  __ \  \/_/\ \/ \ \ \  \ \ \/\ \  \ \ \-.  \  \ \___  \ # 
#  \ \_\ \ \_\  \ \_____\    \ \_\  \ \_\ \_\    \ \_\  \ \_\  \ \_____\  \ \_\\"\_\  \/\_____\# 
#   \/_/  \/_/   \/_____/     \/_/   \/_/\/_/     \/_/   \/_/   \/_____/   \/_/ \/_/   \/_____/# 
################################################################################################

#########  SECTION #########
class CreatePersonalProtectiveEquipment(graphene.relay.ClientIDMutation):
    personal_protective_equipment = graphene.Field(PersonalProtectiveEquipmentNode)

    class Input:
        name = graphene.String(
            description='Equipment name',
            required=True,
        )
        equipment_model = graphene.String(
            description='Equipment model',
        )
        serial_number = graphene.String(
            description='Serial number',
        )
        description = graphene.String(
            description='Serial description',
            required=True,
        )

    def mutate_and_get_payload(root, info, **_input):  # pylint: disable=no-self-argument
        name = _input.get('name')
        description = _input.get('description')
        
        if not name:
            raise Exception('Name is required!')
        
        if not description:
            raise Exception('Description is requirements!')

        personal_protective_equipment = PersonalProtectiveEquipment(
            name=name,
            description=description,
            serial_number=_input.get('serial_number'),
            equipment_model=_input.get('equipment_model'),
        )
        personal_protective_equipment.save()

        return CreatePersonalProtectiveEquipment(
            personal_protective_equipment=personal_protective_equipment
        )


class CreateJobEquipment(graphene.relay.ClientIDMutation):
    job_equipment = graphene.Field(JobEquipmentNode)

    class Input:
        name = graphene.String(
            description='Equipment name',
            required=True,
        )
        description = graphene.String(
            description='Serial description',
            required=True,
        )
        equipment_model = graphene.String(
            description='Equipment model',
        )
        serial_number = graphene.String(
            description='Serial number',
        )

    def mutate_and_get_payload(root, info, **_input):  # pylint: disable=no-self-argument
        name = _input.get('name')
        description = _input.get('description')
        serial_number = _input.get('serial_number')
        if not name:
            raise Exception('Name is required!')
        
        if not description:
            raise Exception('Description is required!')

        if not serial_number:
            serial_number = None

        job_equipment = JobEquipment(
            name=name,
            description=description,
            serial_number=serial_number,
            equipment_model=_input.get('equipment_model'),
        )
        job_equipment.save()

        return CreateJobEquipment(job_equipment=job_equipment)


class CreateJobGroup(graphene.relay.ClientIDMutation):
    job_group = graphene.Field(JobGroupNode)

    class Input:
        name = graphene.String(
            description='Name group',
            required=True,
        )
        description = graphene.String(
            description="Group description",
            required=True,
        )
    
    def mutate_and_get_payload(root, info, **_input):  # pylint: disable=no-self-argument
        name = _input.get('name')
        description = _input.get('description')

        if not name:
            raise Exception('Name is required!')

        if not description:
            raise Exception('Description is required!')
        job_group = JobGroup(
            name=name,
            description=description,
        )
        job_group.save()

        return CreateJobGroup(job_group=job_group)


class CreateJob(graphene.relay.ClientIDMutation):
    job = graphene.Field(JobNode)

    class Input:
        name = graphene.String(
            description='Name of job!',
            required=True,
        )
        per_meter = graphene.Boolean(
            description='This job can be charged per meter!',
        )
        value_per_meter = graphene.Float(
            description='If can be charged per meter, what is the price of the meter?'
        )
        job_group_id = graphene.String(
            description='Group of job',
            required=True,
        )
        job_equipment_id = graphene.String(
            description='Job equipment ID'
        )
        has_ppe = graphene.Boolean(
            description='Personal Protective Equipment is needed',
            required=True,
        )
        ppe_id = graphene.String(
            description='Personal Protective Equipment ID',
        )

    def mutate_and_get_payload(root, info, **_input):  # pylint: disable=no-self-argument
        job_group_id = get_object_id(_input.get('job_group_id'), 'JobGroupNode')
        job_equipment_id = get_object_id(_input.get('job_equipment_id'), 'JobEquipmentNode')
        ppe_id = get_object_id(_input.get('ppe_id'), 'PersonalProtectiveEquipmentNode')
        name = _input.get('name')
        per_meter = _input.get('per_meter')
        value_per_meter = _input.get('value_per_meter')
        has_ppe = _input.get('has_ppe')
        job_group = JobGroup.objects.get(pk=job_group_id)  # pylint: disable=no-member
        job_equipment = JobEquipment.objects.get(pk=job_equipment_id)  # pylint: disable=no-member
        ppe = PersonalProtectiveEquipment.objects.get(pk=ppe_id)  # pylint: disable=no-member

        if not job_group_id:
            raise Exception('Job group ID is required!')

        if not name:
            raise Exception('Job name is required!')

        if per_meter == True and not value_per_meter:
            raise Exception('Value per meter is required!')

        if has_ppe == True and not ppe:
            raise Exception('Personal Protective Equipment ID is required!')

        job = Job(
            name=_input.get('name'),
            per_meter=_input.get('per_meter'),
            value_per_meter=_input.get('value_per_meter'),
            job_group=job_group,
            job_equipment=job_equipment,
            has_ppe=has_ppe,
            ppe=ppe,
        )
        job.save()

        return CreateJob(job=job)


######### UPDATES SECTION ###########

class UpdateJobEquipment(graphene.relay.ClientIDMutation):
    job_equipment = graphene.Field(JobEquipmentNode)

    class Input:
        id = graphene.String(
            description='Equipment ID',
            required=True,
        )
        name = graphene.String(
            description='Equipment name',
        )
        description = graphene.String(
            description='Equipement description',
        )
        equipment_model = graphene.String(
            description='Equipment model',
        )
        serial_number = graphene.String(
            description='Equipment serial number',
        )

    def mutate_and_get_payload(root, info, **_input):  # pylint: disable=no-self-argument
        _id = get_object_id(_input.get('id'), 'JobEquipmentNode')
        name = _input.get('name')
        description = _input.get('description')
        equipment_model = _input.get('equipment_model')
        serial_number = _input.get('serial_number')

        if not _id:
            raise Exception('ID is required!')

        job_equipments = JobEquipment.objects.get(pk=_id)  # pylint: disable=no-member

        if not name:
            name = job_equipments.name
        
        if not description:
            description = job_equipments.description
        
        if not equipment_model:
            equipment_model = job_equipments.equipment_model

        if not serial_number:
            serial_number = job_equipments.serial_number
        
        job_equipment = JobEquipment(
            id=_id,
            name=name,
            description=description,
            equipment_model=equipment_model,
            serial_number=serial_number,
        )
        job_equipment.save()

        return UpdateJobEquipment(job_equipment=job_equipment)


class UpdatePersonalProtectiveEquipment(graphene.relay.ClientIDMutation):
    personal_protective_equipment = graphene.Field(PersonalProtectiveEquipmentNode)

    class Input:
        id = graphene.String(
            description='PPE ID',
            required=True,
        )
        name = graphene.String(
            description='PPE name',
        )
        description = graphene.String(
            description='PPE description',
        )
        equipment_model = graphene.String(
            description='PPE model',
        )
        serial_number = graphene.String(
            description='PPE Serial number',
        )

    def mutate_and_get_payload(root, info, **_input):  # pylint: disable=no-self-argument
        _id = get_object_id(_input.get('id'), 'PersonalProtectiveEquipmentNode')
        name = _input.get('name')
        description = _input.get('description')
        equipment_model = _input.get('equipment_model')
        serial_number = _input.get('serial_number')

        if not _id:
            raise Exception('PPE ID is required')

        ppe = PersonalProtectiveEquipment.objects.get(pk=_id)  # pylint: disable=no-member

        if not name:
            name = ppe.name

        if not equipment_model:
            equipment_model = ppe.equipment_model
        
        if not description:
            description = ppe.description

        if not serial_number:
            serial_number = ppe.serial_number

        personal_protective_equipment = PersonalProtectiveEquipment(
            id=_id,
            name=name,
            description=description,
            equipment_model=equipment_model,
            serial_number=serial_number,
        )
        personal_protective_equipment.save()

        return UpdatePersonalProtectiveEquipment(
            personal_protective_equipment=personal_protective_equipment
        )


class UpdateJobGroup(graphene.relay.ClientIDMutation):
    job_group = graphene.Field(JobGroupNode)

    class Input:
        id = graphene.String(
            description='Group ID',
            required=True,
        )
        name = graphene.String(
            description="Group name",
        )
        description = graphene.String(
            description="Group description",
        )

    def mutate_and_get_payload(root, info, **_input):  # pylint: disable=no-self-argument
        _id = get_object_id(_input.get('id'), 'JobGroupNode')
        name = _input.get('name')
        description = _input.get('description')

        if not _id:
            raise Exception('Id is required')

        job_groups = JobGroup.objects.get(pk=_id)  # pylint: disable=no-member

        if not _input.get('name'):
            name = job_groups.name
        
        if not _input.get('description'):
            description = job_groups.description


        job_group = JobGroup(
            id=_id,
            name=name,
            description=description,
        )
        job_group.save()

        return CreateJobGroup(job_group=job_group)


class UpdateJob(graphene.relay.ClientIDMutation):
    job = graphene.Field(JobNode)

    class Input:
        id = graphene.String(
            description='Job Id',
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
        job_group_id = graphene.String(
            description='Job group ID!'
        )
        job_equipment_id = graphene.String(
            description='Job equipment ID!'
        )
        has_ppe = graphene.Boolean(
            description="Has personal protective equipment?",
        )
        ppe_id = graphene.String(
            description="Personal protective equipment ID!"
        )
    
    def mutate_and_get_payload(root, info, **_input):  # pylint: disable=no-self-argument
        _id = get_object_id(_input.get('id'), 'JobNode')
        job_equipment_id = get_object_id(_input.get('job_equipment_id'), 'JobEquipmentNode')
        ppe_id = get_object_id(_input.get('ppe_id'), 'PersonalProtectiveEquipmentNode')
        job_group_id = get_object_id(_input.get('job_group_id'), 'JobGroupNode')
        value_per_meter = _input.get('value_per_meter')
        per_meter = _input.get('per_meter')
        name = _input.get('name')
        has_ppe = _input.get('has_ppe')
        jobs = Job.objects.get(pk=_id)  # pylint: disable=no-member
        job_equipment = JobEquipment.objects.get(pk=job_equipment_id)  # pylint: disable=no-member
        ppe = PersonalProtectiveEquipment.objects.get(pk=ppe_id)  # pylint: disable=no-member
        job_group = JobGroup.objects.get(pk=job_group_id)  # pylint: disable=no-member

        if not _id:
            raise Exception('Id is required!')

        if per_meter == True:
            if not value_per_meter:
                raise Exception('Value per meter is required!')

        if not name:
            name = jobs.name

        if value_per_meter:
            if per_meter == False:
                raise Exception('Value per meter is not required!')
        elif not value_per_meter:
            value_per_meter = None

        if has_ppe == True and not ppe:
            raise Exception('Personal protective equipment id is required!')
        elif has_ppe == False and ppe:
            raise Exception('Personal protective equipment id is not required!')
        
        job = Job(
            id=_id,
            name=name,
            per_meter=per_meter,
            value_per_meter=value_per_meter,
            job_group=job_group,
            job_equipment=job_equipment,
            has_ppe=has_ppe,
            ppe=ppe,
        )
        job.save()

        return UpdateJob(job=job)


class Mutation(graphene.AbstractType):
    create_job = CreateJob.Field()
    create_job_equipment = CreateJobEquipment.Field()
    create_job_group = CreateJobGroup.Field()
    create_personal_protective_equipment = CreatePersonalProtectiveEquipment.Field()
    update_job = UpdateJob.Field()
    update_job_equipment = UpdateJobEquipment.Field()
    update_job_group = UpdateJobGroup.Field()
    update_personal_protective_equipment = UpdatePersonalProtectiveEquipment.Field()
