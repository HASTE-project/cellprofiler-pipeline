# We build this base Docker image with the more stable dependencies, so it is cached for faster building during development.


FROM ubuntu:16.04
#FROM cellprofiler/cellprofiler:3.1.8


# See:
# https://github.com/CellProfiler/CellProfiler/wiki/Source-installation-(Ubuntu-16.04-LTS)
# Many dependencies are broken...


# Looks like this is Python 2.

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y \
    build-essential    \
    cython             \
    git                \
    libmysqlclient-dev \
    libhdf5-dev        \
    libxml2-dev        \
    libxslt1-dev       \
    openjdk-8-jdk      \
    python-dev         \
    python-pip         \
    python-h5py        \
    python-matplotlib  \
    python-mysqldb     \
    python-scipy       \
    python-numpy       \
    python-pytest      \
    python-vigra       \
    python-wxgtk3.0
#    python-zmq (this is wrong version by default)




RUN pip install --upgrade pip


#RUN apt install -y openjdk-8-jdk

RUN git clone https://github.com/CellProfiler/CellProfiler.git
#RUN git clone https://github.com/CellProfiler/CellProfiler-plugins.git /CellProfiler-plugins



WORKDIR /CellProfiler
RUN git checkout tags/v3.1.8
RUN pip install -e . ; echo "return ok"

RUN pip freeze

# These dependencies are missing or wrong version.
#RUN pip install --upgrade Pillow
#RUN pip install pyzmq==15.3.0
#RUN pip install setuptools==36.2
#RUN pip install python-dateutil==2.8.0
RUN pip install numpy==1.16.3

# tensorflow==1.13.1 gives this error on Ola's machine:
# "TensorFlow library was compiled to use SSE4.1 instructions, but these aren't available on your machine. Aborted (core dumped)"
# i.e. hardware is too old! Lets try an older version of the from 2018, when the 'measure image focus' plugin was originally developed.
#RUN pip install tensorflow==1.8.0

RUN pip freeze
