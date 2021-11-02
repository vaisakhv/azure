from lib.base import AzureBaseAction

class TagVM(AzureBaseAction):

    def run(self, group_name, vm_name, json_creds):

        credentials, subscription_id = self.get_credentials(json_creds)
        compute_client = ComputeManagementClient(credentials, subscription_id)

        try:
            async_vm_update = compute_client.virtual_machines.create_or_update(
                group_name,
                vm_name,
                {
                    'location': self.LOCATION,
                    'tags': {
                        'who-rocks': 'python',
                        'where': 'on azure'
                    }
                }
            )
            result = {"output": async_vm_update, "message": "VM Tagging successful"}
        except CloudError:
            result = {"error": "A VM operation failed:\n" + traceback.format_exc()}
        else:
            result = {"message": "Tagging-VM operation completed successfully!"}

        return result
