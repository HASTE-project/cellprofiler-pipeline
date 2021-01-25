[![Build Status](https://travis-ci.org/HASTE-project/cellprofiler-pipeline.svg?branch=master)](https://travis-ci.org/HASTE-project/cellprofiler-pipeline)


A simple, distributed, image stream processing pipeline built around CellProfiler, as a case study demonstrating use of the HASTE Toolkit.

The application is intended for 'real time' processing of images from a microscope.

The application comprises a single 'client', which monitors a directory for new images appearing as files on disk, and worker application which invokes CellProfiler.
Each are built and deployed separately as Docker images. The workers can be scaled for parallel processing.


The repo https://github.com/HASTE-project/k8s-deployments contains code which configures and deploys the application, as demonstrated as the first case study in this paper:
```
"Rapid development of cloud-native intelligent data pipelines for scientific data streams using the HASTE Toolkit"
https://www.biorxiv.org/content/10.1101/2020.09.13.274779v1
```

To reproduce the results in the paper, deploy and run the application according to the instructions at https://github.com/HASTE-project/k8s-deployments


Directory structure:

```
client - client application as a python package and Dockerfile.  
worker - worker application as a python package and Dockerfile.
    worker-base - base DockerFile to make it quicker to build the dockerfile for the application itself.
```

To build and push the Docker images manually:
```
docker build -t "benblamey/haste_pipeline_worker_base:latest" ./worker/worker-base 
docker build -t "benblamey/haste_pipeline_worker:latest" ./worker ; docker push "benblamey/haste_pipeline_worker:latest"

docker build --no-cache=true -t "benblamey/haste_pipeline_client:latest" ./client
docker push "benblamey/client:latest
```
