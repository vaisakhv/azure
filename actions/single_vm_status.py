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

class SingleVmStatus(AzureBaseAction):

    def run(self, vm, json_creds):

        credentials, subscription_id = self.get_credentials(json_creds)
        compute_client = ComputeManagementClient(credentials, subscription_id)
        result = {}
        try:
            for v in compute_client.virtual_machines.list_all():
                if v.name == vm:
                    vm_details = v.id.split("/")
                    res_grp = vm_details[4]
                    vm_name = vm_details[-1]
                    statuses = compute_client.virtual_machines.instance_view(res_grp, vm_name).statuses
                    status = len(statuses) >= 2 and statuses[1]
                    state = status.code.split('/')[-1]
                    print("VM Name : {} \n \tState : {} ".format(v.name, state.capitalize()))
                    result = {"status": state}
        except CloudError:
            result = {"error": "A VM operation failed:\n" + traceback.format_exc()}
            # raise result
        return result

