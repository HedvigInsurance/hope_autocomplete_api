FROM python:3.7

RUN mkdir -p /tmp/service
COPY ./ /tmp/service
RUN pip install /tmp/service && rm -rf /tmp/service

ENTRYPOINT run_autocomplete_service