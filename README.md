## Project Overview

This is a sample project for providing HTTP status of a web page in Prometheus format

## Project Structure

The project consists of:

* Main python project, creating the service to get status from external URLs
* `Dockerfile` to create a docker image
* Helm chart for easy deployment on Kubernetes clusters

## How to run locally

You may run the project locally either from source or in a docker container.

### From source code

1. Install python (https://www.python.org/downloads/)
2. You might also need to install `pip`.

    a. Ubuntu: `sudo apt update && sudo apt install python3-pip`
    b. MacOS: `brew install python` (pip is part of this formula)

3. Navigate to the project root directory, install dependencies and run the project.

    ```shell
    user@host:~$ pip install -r requirements.txt
    user@host:~$ python run.py
    ```

    > You might need to run `python3 run.py`

3. You should see a message like:

    ```shell
    user@host:~$ python3 run.py
    Prometheus metrics available on port 8000 /metrics
    HTTP server available on port 8001
    ```

### In a container

1. Install docker (https://www.docker.com/)
2. Navigate to the project root directory in order to build and run the image.

    ```shell
    user@host:~$ docker build -t python/http_status_service:0.1.0 .
    user@host:~$ docker run -p 8000:8000 -p 8001:8001 python/http_status_service:0.1.0 .
    ```

In both cases you may open your web browser and navigate to http://localhost:8000 and http://localhost:8001 to view the respective services.

## How to create a Helm chart

1. Install Helm (https://helm.sh/docs/intro/install/)
2. Navigate to the project root directory in order to create the chart.

    ```shell
    user@host:~$ helm create httpstatus
    ```

3. Navigate to Helm chart directory
4. Open `Chart.yaml`. You might want to review/modify `name`, `version` and/or `appVersion`.
5. Open `values.yaml`

    a. Set the `repository` from witch the image will be pulled

    b. Set the `tag` as needed

    c. Check the service property. You night need to set its `type` as `NodePort` and also modify the `port` to the one the simple HTTT server is running (by default `8001`)

    d. For security reasons you might want to run the application as a non-root user. Under `securityContext` check and modify `runAsNonRoot: true` and set the `runAsUser` to the UID of the user as it is set in the `Dockerfile`

    e. You might also want to configure ingress in order to access the service from the internet, but this is out of scope of this assessment.

## How to deploy a Helm chart

In order to deploy a Helm chart to a Kubernetes cluster

1. Provided that `kubectl` is installed and you already have credentials to a few Kubernetes clusters, use `kubectl config use-context [context]` to point to the right cluster on which to deploy the chart.

2. Issue command

    ```shell
    user@host:~$ helm install -f ./path_to_your_chart/values.yaml httpstatus ./path_to_your_chart
    ```

## NOTES

Next steps might include

1. Set a process in order to properly

    a. build, test, package the source code (artifact)

    b. deploy artifact to artifactory

    c. build the docker image using the artifact rather than source code

2. Provide instructions on setting up a local k8s cluster (either minikube or Docker Desktop) for local testing/troubleshouting.

3. Automate whatever can be automated!