# block-montecarlo_simulation
FROM python:3
EXPOSE 7004
ENV FLASK_DEBUG=1
ENV PORT=7004
RUN pip install flask
RUN pip install cerberus
RUN pip install requests
RUN pip install beautifulsoup4
RUN pip install lxml