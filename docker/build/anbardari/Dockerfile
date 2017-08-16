FROM registry.cafebazaar.ir:5000/common-images/ubuntu:trusty-py2-django


# Get Gunicorn port as ARG
#ARG gunicorn_port

# Add files
ADD . /opt/dbproject

# Expose port
#EXPOSE $gunicorn_port
EXPOSE 54333

# Switch to project dir
WORKDIR /opt/dbproject

# Add CMD
CMD python anbardari_service.py start

# Install pip dependencies
RUN pip install -r requirements-prod.txt

# Make scripts executable & Create Gunicorn dir
RUN \
    chmod +x manage.py && \
    chmod +x anbardari_service.py && \
    mkdir -p /etc/gunicorn
