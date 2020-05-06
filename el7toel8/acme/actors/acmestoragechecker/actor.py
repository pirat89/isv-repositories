from leapp import reporting
from leapp.actors import Actor
from leapp.models import Report, AcmeStorageInfo
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag


class AcmeStorageChecker(Actor):
    """
    Report change in ACME storage on RHEL 8 if ACME storage is used
    """

    name = 'acme_storage_checker'
    consumes = (AcmeStorageInfo,)
    produces = (Report,)
    tags = (ChecksPhaseTag, IPUWorkflowTag)

    def process(self):
        # Check if Acme is installed and used
        acme_info = next(self.consume(AcmeStorageInfo), None)
        if not acme_info:
            return

        # Inform the system administrator about the change
        if acme_info.has_device and acme_info.has_kernel_module:
            reporting.create_report([
                reporting.Title('ACME Storage device path migration'),
                reporting.Summary('ACME Storage device path is going to change to /dev/acme'),
                reporting.Severity(reporting.Severity.INFO),
                reporting.Tags([reporting.Tags.OS_FACTS]),
                reporting.RelatedResource('device', '/dev/acme0'),
                reporting.RelatedResource('device', '/dev/acme'),
                reporting.ExternalLink(
                    url='https://acme.corp/storage-rhel',
                    title='ACME Storage on RHEL'
                )
            ])
        elif acme_info.has_device and not acme_info.has_kernel_module:
            self.log.warning(
                'Acme storage device detected but kernel module is not loaded.'
            )
