FROM python:3.7.2-stretch
RUN pip install websockets
COPY *ipeRis*.py /bin/
RUN chmod 0755 /bin/*ipeRis*
RUN cd /bin
ENTRYPOINT ["python", "/bin/ripeRisLive.py"]
