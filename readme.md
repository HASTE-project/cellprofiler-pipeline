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



Directory structure:

```
client - client application as a python package and Dockerfile.  
worker - worker application as a python package and Dockerfile.
    worker-base - base DockerFile to make it quicker to build the dockerfile for the application itself.
```

To build and push the Docker images:
```
docker build -t "benblamey/haste_pipeline_worker_base:latest" ./worker/worker-base 
docker build -t "benblamey/haste_pipeline_worker:v2" ./worker ; docker push "benblamey/haste_pipeline_worker:v2"

docker build --no-cache=true -t "benblamey/haste_pipeline_client:latest" ./client
docker push "benblamey/haste_pipeline_worker_base:v2"
```



# Developer Notes

To run locally (for development):

```
# Install:

python2 -m pip install --user -e ./worker
python3 -m pip install -e ./client

# Start rabbitmq:
rabbitmq-server

rabbitmqadmin delete queue name='files'

# Start the worker:
python2 -m haste.pipeline.worker --host localhost /Users/benblamey/projects/haste/haste-desktop-agent-images/target

# Start the client:
python3 -m haste.pipeline.client --include png --tag foo --host localhost /Users/benblamey/projects/haste/haste-desktop-agent-images/target

# Stop rabbitmq
rabbitmqctl stop
```


To run locally, with containers:
```

docker run benblamey/haste_pipeline_client:latest --include png --tag foo --host localhost /Users/benblamey/projects/haste/haste-desktop-agent-images

docker run benblamey/haste_pipeline_worker:v2 

docker run -it --entrypoint=/dry-run/run-imagequality.sh benblamey/haste_pipeline_worker:latest -i
docker run -it --entrypoint=/bin/bash benblamey/haste_pipeline_worker:latest -i
docker run benblamey/haste_pipeline_worker:latest

# run cellprofiler to test ('dry-run') - with 'OutOfFocus' - requires plugins
python2 -m cellprofiler -c  \
--plugins-directory /CellProfiler-plugins \
-p ../dry-run/OutOfFocus-TestImages.cppipe \
--file-list /dry-run/file-list.txt \
-o .

# run cellprofiler to test ('dry-run') - with 'MeasureImageFocus' - doesn't require plugins

# with plugins
python2 -m cellprofiler -c  \
--plugins-directory /CellProfiler-plugins \
-p /dry-run/MeasureImageQuality-TestImages.cppipe \
--file-list /dry-run/file-list.txt \
-o .

# without plugins
python2 -m cellprofiler -c  \
-p /dry-run/MeasureImageQuality-TestImages.cppipe \
--file-list /dry-run/file-list.txt \
-o .

# run python script, with dev default config:
docker run benblamey/haste_pipeline_worker:latest


```
Note: this will take a bit of RAM.
If you see complaints on memory then "Killed", bump the mem allowed by docker, and restart.

