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
    goblet_version = sys.argv[8]

    # install desired version og goblet
    if goblet_version == "latest":
        pip = subprocess.run(["pip", "install", "goblet-gcp"], capture_output=True)
        if pip.returncode != 0:
            raise Exception(pip.stderr)
    else:
        pip = subprocess.run(["pip", "install", f"goblet-gcp=={goblet_version}"], capture_output=True)
        if pip.returncode != 0:
            raise Exception(pip.stderr)
    os.chdir(goblet_path)
    pip = subprocess.run(["pip", "install", "-r", "requirements.txt"], capture_output=True)
    if pip.returncode != 0:
        raise Exception(pip.stderr)
    
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
    goblet = subprocess.run(command.strip().split(), capture_output=True)

    # Set openapispec output 
    files = glob.glob(".goblet/*.yml")
    if len(files) >= 1:
        with open(files[0], 'r') as f:
            openapi_spec = f.read().replace("%","%25").replace("\n","%0A").replace("\r","%0D")
            if "GITHUB_OUTPUT" in os.environ:
                with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                    print(f"openapispec={openapi_spec}", file=f)

    if goblet.returncode != 0:
        raise Exception(goblet.stderr)
