FROM python:3.7.2-stretch
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY init.sh *ipeRis*.py /bin/
RUN chmod 0755 /bin/*ipeRis* /bin/init.sh
RUN cd /bin
ENTRYPOINT ["init.sh", "python", "/bin/ripeRisLive.py"]
