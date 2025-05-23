FROM ubuntu:22.04

RUN apt-get update

# Set the working directory in the container
WORKDIR /app

# Install blender & bpy
RUN apt-get -y install python3
RUN apt-get -y install blender
RUN apt-get -y install python3-pip
RUN apt-get -y install libsm6 libegl1
RUN pip3 install bpy==3.6.0
RUN pip3 install Pillow
RUN pip3 install fastapi[standard]
RUN pip3 install sqlalchemy

# mysql
RUN pip3 install mysql-connector-python 

EXPOSE 8000:8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]