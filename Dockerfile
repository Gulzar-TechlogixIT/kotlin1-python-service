FROM python:3.12-slim
WORKDIR /app

COPY py_lib1/ /tmp/py_lib1/
COPY py_lib2/ /tmp/py_lib2/
COPY kotlin1-python-service/ /tmp/kotlin1-python-service/

RUN pip install --no-cache-dir \
    /tmp/py_lib1 /tmp/py_lib2 /tmp/kotlin1-python-service

ENV PORT=8087
EXPOSE 8087
CMD ["python", "-m", "kotlin1_python_service.server"]
