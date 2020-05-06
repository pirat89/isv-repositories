import os

from leapp.actors import Actor
from leapp.exceptions import StopActorExecutionError
from leapp.libraries.common.rpms import has_package
from leapp.models import AcmeStorageInfo, ActiveKernelModulesFacts, InstalledRPM
from leapp.tags import FactsPhaseTag, IPUWorkflowTag


class AcmeStorageScanner(Actor):
    """
    Scan the system for ACME Storage
    """

    name = 'acme_storage_scanner'
    consumes = (ActiveKernelModulesFacts, InstalledRPM)
    produces = (AcmeStorageInfo)
    tags = (FactsPhaseTag, IPUWorkflowTag)

    def process(self):
        # Check if our package is installed
        if not has_package(InstalledRPM, 'acme-storage'):
            return

        # Get a list of active kernel modules
        kernel_module_facts = next(self.consume(ActiveKernelModulesFacts), None)
        if not kernel_module_facts:
            # hypothetic error; it should not happen
            raise StopActorExecutionError('Unable to obtain list of active kernel modules.')
            return

        # Detect if our kernel module is installed
        has_kernel_module = False
        for active_module in kernel_module_facts.kernel_modules:
            if active_module.filename == 'acme8xx':
                has_kernel_module = True
                break

        # Is the device installed in the default location?
        has_device = os.path.exists('/dev/acme0')

        self.produce(AcmeStorageInfo(has_kernel_module=has_kernel_module, has_device=has_device))
