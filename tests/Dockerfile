FROM python:3.11

WORKDIR /app

ENV PIP_ROOT_USER_ACTION ignore
ENV PIP_NO_CACHE_DIR 1
ENV PYTHONPATH=/app/
ENV PYTHONUNBUFFERED=1

COPY ./tests/requirements.txt ./requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY parsley parsley
COPY tests tests

CMD ["pytest", "-s", "tests/src/"]
