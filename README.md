# Goblet Github Action

This Github action allows automated deployment of your Goblet application via Github Actions.

[Goblet](https://github.com/goblet/goblet) is a framework for writing serverless rest apis in python in google cloud. It allows you to quickly create and deploy python apis backed by cloudfunctions.

## Parameters

The parameters will be passed to the action through `with`

| Name           | Description                                                                                                                        | Required?  |
|----------------|------------------------------------------------------------------------------------------------------------------------------------|---|
| project        | GCP project                                                                                                                        | Required  |
| location       | GCP location                                                                                                                       | Required  |
| goblet-path    | Path to a goblet app directory in which `main.py`, `requirements.txt` and `.goblet\` should be stored                              | Optional  |
| stage          | Name of stage which should be used                                                                                                 | Optional  |
| envars         | list of key, value pairs that should be added to the function's environment variables (written as '{k1}:{v1},{k2}:{v2},...')       | Optional
| build-envars   | list of key, value pairs that should be added to the function's build environment variables (written as '{k1}:{v1},{k2}:{v2},...') | Optional
| command        | Complete goblet command. For example "goblet openapi FUNCTION"                                                                     | Optional
| artifact-auth  | Enable authentication to Artifact Registry.                                                                                        | Optional
| poetry         | [yes/no] enable use of poetry as dependency management. Default no.                                                                | Optional
| poetry_version | version for poetry. Default 1.1.14.                                                                                                | Optional
| requirements   | Path and filename to requirements file for pip install. Default requirements.txt                                                   | Optional

## Outputs


| Name  | Description  |
|---|---|
| openapispec  | The full string output of the generated openapispec if one was created  |

## Usage

1. Create a directory named `.github/workflow/`

2. Create a YAML file, e.g. action_workflow.yml, and place it in the created directory above 
(requires a step `actions/checkout@v2` to get goblet app and `google-github-actions/auth@v0` to 
get credentials)

3. Example content of the YAML file:

```
on:
  push:
    branches:
      - main
name: Deploy Goblet App
jobs:
  deploy:
    name: deploy
    runs-on: ubuntu-latest
    env:
      GCLOUD_PROJECT: GCLOUD_PROJECT
    steps:
    - name: checkout
      uses: actions/checkout@v2
    - id: 'auth'
      uses: 'google-github-actions/auth@v0'
      with:
        workload_identity_provider: 'projects/123456789/locations/global/workloadIdentityPools/my-pool/providers/my-provider'
        service_account: 'my-service-account@my-project.iam.gserviceaccount.com'
    - name: goblet deploy
      uses: anovis/goblet-github-actions@v3.0
      id: deploy
      with:
        project: ${{ env.GCLOUD_PROJECT }}
        location: us-central1
        goblet-path: test
        stage: dev
        envars:  |-
          SLACK_WEBHOOK:slack,BILLING_ORG:bill,BILLING_ID:bill_id
    - name: echo openapispec
      run: |
        echo "${{steps.deploy.outputs.openapispec}}"

```


## Service Account

The recommendation is to set the GCP service account json file as a GitHub secret in your GitHub repository.
Make sure the service account has the correct permissions to deploy the desired components. At a miminum it should include

* roles/cloudfunctions.admin
* roles/iam.serviceAccountUser


## Requirements file

Starting from version 3.0 a requirements file is mandatory (if not provided,
requirements.txt will be used). This is why goblet version parameter is no longer necessary.  
The version for Goblet must be defined in the correspondant requirements file 
as usually; eg:

``` Python
goblet-gcp==0.10.0
```

In case of poetry=yes you should add also poetry_version argument


The install of dependencies defined in the requirements file is at the first step
in the git-hub-action ensuring Goblet is installed at the moment of the 
deployment.

If you choose poetry, Goblet will not be installed at all unless you 
included it in the dependency install using poetry.



