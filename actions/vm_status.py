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

class VMstatus(AzureBaseAction):
    
    #credentials, subscription_id = self.get_credentials()
    #compute_client = ComputeManagementClient(credentials, subscription_id)
    
    def run(self, json_creds):

        credentials, subscription_id = self.get_credentials(json_creds)
        compute_client = ComputeManagementClient(credentials, subscription_id)

        try:
            # print('\nList VM's status in subscription')
	    for vm in compute_client.virtual_machines.list_all():
	        print("\tVM Name : {} \n \tState : {} ".format(vm.name, self.get_vm_state(vm)))
	    result = {"message": "success"}
				
        except CloudError:
            result = {"error": "A VM operation failed:\n" + traceback.format_exc()}
			#raise result
        return result
		
    def get_vm_state(self, vm):
        credentials, subscription_id = self.get_credentials()
        compute_client = ComputeManagementClient(credentials, subscription_id)
	vm_details = vm.id.split("/")
	res_grp = vm_details[4]
	vm_name = vm_details[-1]
	statuses = compute_client.virtual_machines.instance_view(res_grp, vm_name).statuses
	status = len(statuses) >= 2 and statuses[1]
	state = status.code.split('/')[-1]
	return state.capitalize()


