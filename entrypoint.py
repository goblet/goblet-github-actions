import sys
import json
import subprocess

if __name__ == "__main__":
    project = sys.argv[1]
    location = sys.argv[2]
    stage = sys.argv[3]
    envars = sys.argv[4]

    stage_sub_command = ""
    config_sub_command = ""
    if stage:
        stage_sub_command = f"--stage {stage}"
    if envars:
        envars_list = envars.split(',')
        config = {
            "cloudfunction": {
                "environmentVariables": {}
            }
        }
        for envar in envars_list:
            try:
                key, value = envar.split(':', 1)
                config["cloudfunction"]["environmentVariables"][key] = value
            except ValueError:
                raise "Environment variables are in the wrong format. Should be '{k1}:{v1},{k2}:{v2},...'"
        config_sub_command = f"--config-from-json-string {json.dumps(config, separators=(',', ':'))}"

    command = f"goblet deploy --project {project} --location {location} {stage_sub_command} {config_sub_command}"
    # subprocess takes in list of strings. strip to get rid of white space from undefined, optional fields
    subprocess.run(command.strip().split())
