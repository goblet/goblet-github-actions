import os
import sys
import json
import subprocess
import glob

if __name__ == "__main__":
    project = sys.argv[1]
    location = sys.argv[2]
    goblet_path = sys.argv[3]
    stage = sys.argv[4]
    envars = sys.argv[5]
    build_envars = sys.argv[6]
    custom_command = sys.argv[7]
    artifact_auth = sys.argv[8]
    poetry = sys.argv[9]
    poetry_version = sys.argv[10]
    requirements_file = sys.argv[11]
    apt_packages = sys.argv[12]

    if apt_packages:
        command = ["apt-get", "install", "-y"]
        command.extend([package.strip() for package in apt_packages.split(',')])
        apt = subprocess.run(command, capture_output=True)
        if apt.returncode != 0:
            raise Exception(apt.stderr)

    # install desired version og goblet
    if artifact_auth == "yes":
        pip = subprocess.run(["pip", "install", "keyrings.google-artifactregistry-auth==1.1.1"], capture_output=True)
        if pip.returncode != 0:
            raise Exception(pip.stderr)

    os.chdir(goblet_path)

    if poetry != "yes":
        if requirements_file == "":
            requirements_file = "requirements.txt"
        pip = subprocess.run(["pip", "install", "-r", requirements_file], capture_output=True)
        if pip.returncode != 0:
            raise Exception(pip.stderr)
    elif poetry == "yes" and poetry_version != "":
        pip_install_poetry = subprocess.run(["pip", "install", f"poetry=={poetry_version}"], capture_output=True)
        poetry_config = subprocess.run(["poetry", "config", "virtualenvs.create", "false"], capture_output=True)
        poetry_install = subprocess.run(["poetry", "install", "--only", "main", "--no-root"], capture_output=True)
        poetry_requirements = subprocess.run(["poetry", "export", "-f", "requirements.txt", "-o", "requirements.txt"], capture_output=True)
        if pip_install_poetry.returncode != 0 or poetry_config.returncode != 0 or poetry_install.returncode != 0 or poetry_requirements.returncode != 0:
            raise Exception(
                [f"PIP INSTALL STDERR returncode= {pip_install_poetry.returncode} {pip_install_poetry.stderr}",
                 f"POETRY CONFIG STDERR returncode= {poetry_config.returncode} {poetry_config.stderr}",
                 f"POETRY INSTALL STDERR returncode= {poetry_install.returncode} {poetry_install.stderr}",
                 f"POETRY REQUIREMENTS STDERR returncode= {poetry_requirements.returncode} {poetry_requirements.stderr}"
                 ]
            )

    stage_sub_command = ""
    config_sub_command = ""
    if stage:
        stage_sub_command = f"--stage {stage}"
    if envars or build_envars:
        config = {
            "cloudfunction": {
                "environmentVariables": {},
                "buildEnvironmentVariables": {}
            }
        }
        if envars:
            envars_list = envars.split(',')
            for envar in envars_list:
                try:
                    key, value = envar.split(':', 1)
                    config["cloudfunction"]["environmentVariables"][key] = value
                except ValueError:
                    raise "Environment variables are in the wrong format. Should be '{k1}:{v1},{k2}:{v2},...'"
        if build_envars:
            build_envars_list = build_envars.split(',')
            for build_envar in build_envars_list:
                try:
                    key, value = build_envar.split(':', 1)
                    config["cloudfunction"]["buildEnvironmentVariables"][key] = value
                except ValueError:
                    raise "Build Environment variables are in the wrong format. Should be '{k1}:{v1},{k2}:{v2},...'"
        config_sub_command = f"--config-from-json-string {json.dumps(config, separators=(',', ':'))}"

    if custom_command:
        command = custom_command
    else:
        command = f"goblet deploy --project {project} --location {location} {stage_sub_command} {config_sub_command}"
    # subprocess takes in list of strings. strip to get rid of white space from undefined, optional fields
    print(f"Running command {command}")
    goblet = subprocess.run(command.strip().split(), capture_output=True)

    # Set openapispec output 
    files = glob.glob(".goblet/*.yml")
    if len(files) >= 1:
        with open(files[0], 'r') as f:
            openapi_spec = f.read().replace("%", "%25").replace("\n", "%0A").replace("\r", "%0D")
            if "GITHUB_OUTPUT" in os.environ:
                with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                    print(f"openapispec={openapi_spec}", file=f)

    if goblet.returncode != 0:
        raise Exception(f"Goblet deploy returncode {goblet.returncode}. Messsage Stderr: {goblet.stderr} Messsage Stdout: {goblet.stdout}")
