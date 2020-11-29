FROM python:3.6-slim
#install Linux Debian and then installs Python 3.6 on top of it.
WORKDIR /app
#roughly the equivalent of mkdir app upon creation of the container
ADD . /app
#copy all files (e.g. app.py, Dockerfile, requirements.txt and move into /app)
RUN pip install --trusted-host pypi.python.org -r requirements.txt
#install all python libraries that you find in the file called requirements.txt
CMD ["python", "etl.py"]
#run the source code