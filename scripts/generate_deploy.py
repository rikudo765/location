from jinja2 import Template
import subprocess

subprocess.run(["git", "checkout", "master"])
version_tag = subprocess.check_output(["git", "log", "-1", "--pretty=%h"], encoding="utf-8")[0:-1]
project_id = subprocess.check_output(["gcloud", "config", "get-value", "project"], encoding="utf-8")[0:-1]

deployment_template = Template(open('./scripts/deployment_template.yaml').read())

deployment = deployment_template.render(VERSION_TAG=str(version_tag), PROJECT_ID=str(project_id))
with open("./deployment.yaml", 'w') as file:
    file.write(deployment)

deployment_script = "#!/bin/bash\n" \
                    "echo Deploying version with tag: {1}\n"\
                    "docker build -t gcr.io/{0}/location:{1} .\n" \
                    "docker push gcr.io/{0}/location:{1}\n" \
                    "kubectl apply -f deployment.yaml".format(project_id, version_tag)

with open("./run_deployment.sh", 'w') as file:
    file.write(deployment_script)

subprocess.run(["chmod", "u+x", "./run_deployment.sh"])
