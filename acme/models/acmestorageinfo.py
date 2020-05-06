from leapp.models import Model, fields
from leapp.topics import SystemFactsTopic


class AcmeStorageInfo(Model):
    topic = SystemFactsTopic

    has_kernel_module = fields.Boolean()
    has_device = fields.Boolean()
