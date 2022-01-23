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


    os.chdir(goblet_path)
    pip = subprocess.run(["pip", "install", "-r", "requirements.txt"], capture_output=True)
    if pip.returncode != 0:
        raise Exception(pip.stderr)
    
    stage_sub_command = ""
    config_sub_command = ""
    if stage:
        stage_sub_command = f"--stage {stage}"
    if envars or build_envars:
        envars_list = envars.split(',')
        build_envars_list = build_envars.split(',')
        config = {
            "cloudfunction": {
                "environmentVariables": {},
                "buildEnvironmentVariables": {}
            }
        }
        for envar in envars_list:
            try:
                key, value = envar.split(':', 1)
                config["cloudfunction"]["environmentVariables"][key] = value
            except ValueError:
                raise "Environment variables are in the wrong format. Should be '{k1}:{v1},{k2}:{v2},...'"
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
            output_command = ["echo",f"::set-output name=openapispec::{f.read()}"]
        subprocess.run(output_command, capture_output=True)

    if goblet.returncode != 0:
        raise Exception(goblet.stderr)
