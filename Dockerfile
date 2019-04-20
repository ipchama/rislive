FROM python:3.7.2-stretch
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY *ipeRis*.py /bin/
RUN chmod 0755 /bin/*ipeRis*
RUN cd /bin
ENTRYPOINT ["python", "/bin/ripeRisLive.py"]
