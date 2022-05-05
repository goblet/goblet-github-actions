# Goblet Github Action

This Github action allows automated deployment of your Goblet application via Github Actions.

[Goblet](https://github.com/anovis/goblet) is a framework for writing serverless rest apis in python in google cloud. It allows you to quickly create and deploy python apis backed by cloudfunctions.

## Parameters

The parameters will be passed to the action through `with`

| Name  | Description  | Required?  |
|---|---|---|
| project  | GCP project  | Required  |
| location  | GCP location  | Required  |
| goblet_path  | Path to a goblet app directory in which `main.py`, `requirements.txt` and `.goblet\` should be stored  | Optional  |
| stage  | Name of stage which should be used | Optional  |
| envars | list of key, value pairs that should be added to the function's environment variables (written as '{k1}:{v1},{k2}:{v2},...') | Optional
| buildEnvars | list of key, value pairs that should be added to the function's build environment variables (written as '{k1}:{v1},{k2}:{v2},...') | Optional
| command | Complete goblet command. For example "goblet openapi FUNCTION" | Optional

## Outputs


| Name  | Description  |
|---|---|
| openapispec  | The full string output of the generated openapispec if one was created  |

## Usage

1. Create a directory named `.github/workflow/`

2. Create a YAML file, e.g. action_workflow.yml, and place it in the created directory above 
(requires a step `actions/checkout@v2` to get goblet app and `google-github-actions/setup-gcloud@v0.2.0` to 
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
    - name: Setup Cloud SDK
      uses: google-github-actions/setup-gcloud@v0.2.0
      with:
        project_id: ${{ env.GCLOUD_PROJECT }}
        service_account_key: ${{ secrets.GCP_SA_KEY }}
        export_default_credentials: true
    - name: goblet deploy
      uses: anovis/goblet-github-actions@v2.5
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
