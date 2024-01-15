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

github_repo_owner = "AkashBalani"
github_repo_name = "refactored-meme"
github_token = os.environ.get('GITHUB_ACCESS_TOKEN')
azure_devops_pat = os.environ.get('AZURE_DEVOPS_PAT')

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
os.system(f"gh secret set GITHUB_TOKEN -b {github_token} -r {github_repo_owner}/{github_repo_name}")


