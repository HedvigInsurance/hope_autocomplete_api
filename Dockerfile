FROM python:3.7

RUN mkdir -p /tmp/service
COPY ./ /tmp/service
RUN pip install /tmp/service && rm -rf /tmp/service
RUN python -m nltk.downloader punkt

ENTRYPOINT run_autocomplete_service