import os
import traceback
import yaml
import json

from st2common.runners.base_action import Action

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.models import DiskCreateOption

from msrestazure.azure_exceptions import CloudError

from haikunator import Haikunator

haikunator = Haikunator()

# Azure Datacenter
LOCATION = 'westus'

# Resource Group
GROUP_NAME = 'azure-sample-group-virtual-machines'

# Network
VNET_NAME = 'azure-sample-vnet'
SUBNET_NAME = 'azure-sample-subnet'

# VM
OS_DISK_NAME = 'azure-sample-osdisk'
STORAGE_ACCOUNT_NAME = haikunator.haikunate(delimiter='')

IP_CONFIG_NAME = 'azure-sample-ip-config'
NIC_NAME = 'azure-sample-nic'
USERNAME = 'userlogin'
PASSWORD = 'Pa$$w0rd91'
VM_NAME = 'VmName'

VM_REFERENCE = {
	'linux': {
		'publisher': 'Canonical',
		'offer': 'UbuntuServer',
		'sku': '16.04.0-LTS',
		'version': 'latest'
	},
	'windows': {
		'publisher': 'MicrosoftWindowsServer',
		'offer': 'WindowsServer',
		'sku': '2016-Datacenter',
		'version': 'latest'
	}
}

azure_config ={
	'compute' : {
		'subscription_id': '6688190c-a05f-4ebd-bced-cee2c8b53b35'
	},
	
	'resource_manager' : {
		'client_id' : 'abb0552a-b03d-40aa-873c-322059ab7177',
		'secret' : '50c77e10-4a4c-439c-b482-dd30d949fea6',
		'tenant' : '53f9d213-5534-4788-ac8a-56e81fb1cbc6',
		'default_resource_group' : 'AthenaQAResourceGroup',
	},
	
	'user': {
		'username' : 'fe58c159-583e-474f-bfa7-dc44741e1f86',
		'password' : 'e7hyalQQ_569D=hhtvX=hUB.?DyEY]rG'
		}
	
}

class AzureBaseAction(Action):
	def __init__(self, config):
		super(AzureBaseAction, self).__init__(config=config)
		
	# def get_credentials(self):
		
		# subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
		# credentials = ServicePrincipalCredentials(
			# client_id=os.environ['AZURE_CLIENT_ID'],
			# secret=os.environ['AZURE_CLIENT_SECRET'],
			# tenant=os.environ['AZURE_TENANT_ID']
		# )
		# return credentials, subscription_id

	def get_credentials(self, json_creds):
		subscription_id = json_creds["Subscription_id"]
		credentials = ServicePrincipalCredentials(
			client_id=json_creds["client_id"],
			secret=json_creds['Secret Value'],
			tenant=json_creds["Tenant"]
		)
		return credentials, subscription_id

