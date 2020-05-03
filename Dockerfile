FROM jesusvasquez333/ubuntu1804-epics-base:R3.15.5

# Install system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Point PyEPICS to the libca library
ENV PYEPICS_LIBCA /usr/local/src/epics/base-3.15.5/lib/linux-x86_64/libca.so

# Install python packages
RUN pip3 install \
    flask \
    pyepics \
    matplotlib

# Flask need these variables set in the environment
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Copy the application source code
COPY app.py /app.py

# Set the entrypoint
ENTRYPOINT ["python3", "app.py"]
