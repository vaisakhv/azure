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


class ListVM(AzureBaseAction):

    def run(self, json_creds):

        credentials, subscription_id = self.get_credentials(json_creds)
        compute_client = ComputeManagementClient(credentials, subscription_id)

        try:
            # print('\nList VMs in subscription')
            list_vm = []
            for vm in compute_client.virtual_machines.list_all():
                print("VM : {}".format(vm.name))
                list_vm.append(vm.name)
	    print("No. of VMs:", len(list_vm))
            result = {"output": list_vm, "message": "VM listing successful"}
        except CloudError:
            result = {"error": "A VM operation failed:\n" + traceback.format_exc()}
        else:
            result = {"message": "listing VMs operation completed successfully!"}
        return result
