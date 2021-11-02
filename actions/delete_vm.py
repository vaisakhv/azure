import os
import traceback

from st2common.runners.base_action import Action
from lib.base import AzureBaseAction

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.models import DiskCreateOption

from msrestazure.azure_exceptions import CloudError

from haikunator import Haikunator


class DeleteVM(AzureBaseAction):

    def run(self, group_name, vm_name, json_creds):

        credentials, subscription_id = self.get_credentials(json_creds)
        compute_client = ComputeManagementClient(credentials, subscription_id)

        try:
            # Start the VM
            async_vm_delete = compute_client.virtual_machines.delete(
                group_name, vm_name)
            result = {"output": async_vm_delete, "message": vm_name + "VM creation successful"}
        except CloudError:
            result = {"error": "A VM operation failed:\n" + traceback.format_exc()}
        else:
            result = {"message": "Delete-VM operation completed successfully!"}

        return result
