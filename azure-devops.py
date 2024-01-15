import os

azure_devops_project = "Pipeline_Project"
azure_devops_organization = "balaniaakash"

# Create Azure DevOps Project
os.system(f"az devops project create --name {azure_devops_project} --organization https://dev.azure.com/{azure_devops_organization}")

