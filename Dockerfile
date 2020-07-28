FROM python:3.6
# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
ADD . /code/
WORKDIR /code
RUN pip install -r requirements/development.txt
RUN chmod +x start.sh
# check if mysql is ready and migrate
ENTRYPOINT ["/code/start.sh"]
