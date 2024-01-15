import os

azure_devops_project = "Pipeline_Project"
azure_devops_organization = "balaniaakash"

# Check if the project already exists
project_exists = os.system(f"az devops project show -p {azure_devops_project} --organization https://dev.azure.com/{azure_devops_organization}")

if project_exists != 0:
    # Create Azure DevOps Project if it doesn't exist
    os.system(f"az devops project create --name {azure_devops_project} --organization https://dev.azure.com/{azure_devops_organization}")
    print(f"Azure DevOps project '{azure_devops_project}' created successfully.")
else:
    print(f"Azure DevOps project '{azure_devops_project}' already exists.")


build_pipeline_yaml = """
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- script: echo Hello, world!
  displayName: 'Run a one-line script'
"""

with open("azure-pipelines.yml", "w") as file:
    file.write(build_pipeline_yaml)
