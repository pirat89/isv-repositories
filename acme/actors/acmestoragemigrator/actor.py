from leapp.actors import Actor
from leapp.models import Report, AcmeStorageInfo
from leapp.tags import ApplicationsPhaseTag, IPUWorkflowTag

from leapp import reporting


import os


class AcmeStorageMigrator(Actor):
    """
    Migrate ACME Storage device from old location to the new one
    """

    name = 'acme_storage_migrator'
    consumes = (AcmeStorageInfo,)
    produces = (Report,)
    tags = (ApplicationsPhaseTag, IPUWorkflowTag)

    def process(self):
        acme_storage_info = next(self.consume(AcmeStorageInfo),None)

        # Rename the device
        if acme_storage_info.has_device and acme_storage_info.has_kernel_module:
            os.rename('/dev/acme0', '/dev/acme')

            # Emit a report message informing the system administrator that the device
            # path has been changed
            reporting.create_report([
                reporting.Title('ACME Storage device path migrated'),
                reporting.Summary('ACME Storage device path has been changed to /dev/acme'),
                reporting.Severity(reporting.Severity.INFO),
                reporting.Tags([reporting.Tags.OS_FACTS]),
                reporting.RelatedResource('device', '/dev/acme'),
                reporting.ExternalLink(
                    url='https://acme.corp/storage-rhel',
                    title='ACME Storage on RHEL'
                )
            ])



