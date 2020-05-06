from leapp.actors import Actor
from leapp.models import Report, AcmeStorageInfo, ActiveKernelModulesFacts, InstalledRPM
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag
from leapp.libraries.common.rpms import has_package

from leapp import reporting


import os


class AcmeStorageScanner(Actor):
    """
    Actor that scans if the system contains ACME Storage 
    """

    name = 'acme_storage_scanner'
    consumes = (ActiveKernelModulesFacts,InstalledRPM)
    produces = (Report, AcmeStorageInfo)
    tags = (ChecksPhaseTag, IPUWorkflowTag)

    def process(self):
        # Check if our package is installed
        if not has_package(InstalledRPM, 'acme-storage'):
            return

        # Get a list of active kernel modules
        kernel_module_facts = next(self.consume(ActiveKernelModulesFacts), None)
        if not kernel_module_facts:
            self.log.warning('Unable to obtain list of active kernel modules')
            return

        # Detect if our kernel module is installed
        has_kernel_module = False
        for active_module in kernel_module_facts.kernel_modules:
            if active_module.filename == 'acme8xx':
                has_kernel_module = True
                break

        # Is the device installed in the default location?
        has_device = os.path.exists('/dev/acme0')

        # Inform the system administrator about the change
        if has_device and has_kernel_module:
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

        self.produce(AcmeStorageInfo(has_kernel_module=has_kernel_module, has_device=has_device))

