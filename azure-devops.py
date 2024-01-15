import os
import requests
import base64
import subprocess

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

github_repo_owner = "AkashBalani"
github_repo_name = "refactored-meme"
pipeline_name = "test1"
yaml_path = "azure-pipelines.yml"
github_token = os.environ.get('GITHUB_ACCESS_TOKEN')
azure_devops_pat = os.environ.get('AZURE_DEVOPS_PAT')

github_pat_base64 = base64.b64encode(f"{github_token}:".encode()).decode()

repo_exists = os.system(f"gh repo view {github_repo_owner}/{github_repo_name}")

if repo_exists == 0:
    print(f"GitHub repository '{github_repo_owner}/{github_repo_name}' already exists.")
else:
    # Create GitHub repository if it doesn't exist
    os.system(f"gh repo create {github_repo_owner}/{github_repo_name} --confirm")
    print(f"GitHub repository '{github_repo_owner}/{github_repo_name}' created successfully.")
os.system("git add .")
os.system("git commit -m \"Add Azure Pipelines configuration\"")
os.system("git push origin main")

# Configure GitHub Repository Secrets
os.system(f"gh secret set AZURE_DEVOPS_PAT -b {azure_devops_pat} -r {github_repo_owner}/{github_repo_name}")
os.system(f"gh secret set TOKEN_GH -b {github_token} -r {github_repo_owner}/{github_repo_name}")

def create_azure_devops_service_connection():
    url = f'https://dev.azure.com/{azure_devops_organization}/{azure_devops_project}/_apis/serviceendpoint/endpoints?api-version=7.1-preview.2'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {base64.b64encode(f":{azure_devops_pat}".encode()).decode()}'
    }

    data = {
        'name': 'GitHubConnection',
        'type': 'github',
        'url': f'https://github.com/{github_repo_owner}/{github_repo_name}',
        'authorization': {
            'parameters': {
                'accessToken': azure_devops_pat
            },
            'scheme': 'PersonalAccessToken'
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Azure DevOps service connection created successfully.")
    else:
        print(f"Failed to create Azure DevOps service connection. Status code: {response.status_code}, Error: {response.text}")

create_azure_devops_service_connection()


def create_azure_pipeline():
    try:
        # Command to create an Azure Pipeline
        command = [
            'az', 'pipelines', 'create',
            '--name', pipeline_name,
            '--repository', f'https://dev.azure.com/{azure_devops_organization}/{azure_devops_project}/_git/{github_repo_name}',
            '--yaml-path', yaml_path
        ]

        # Execute the command
        subprocess.run(command, check=True)
        print(f"Azure Pipeline '{pipeline_name}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create Azure Pipeline. Error: {e}")

create_azure_pipeline()
# Trigger Build Pipeline
os.system(f"az pipelines build queue --definition-name azure-pipelines --project {azure_devops_project} --organization https://dev.azure.com/{azure_devops_organization}")



