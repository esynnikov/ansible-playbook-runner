FROM python:3.6


RUN apt-get update
RUN apt-get install sshpass
RUN sed -i 's/#   StrictHostKeyChecking ask/StrictHostKeyChecking no/g' /etc/ssh/ssh_config
RUN echo 'UserKnownHostsFile=/dev/null' >> /etc/ssh/ssh_config
RUN pip install django
RUN pip install ansible
RUN mkdir -p /opt/Projects
RUN mkdir -p /opt/runner

RUN cd /opt/runner && git clone https://github.com/esynnikov/ansible-playbook-runner

RUN chmod -R 777 /opt/runner

EXPOSE 8000


ENTRYPOINT ["python", "/opt/runner/ansible-playbook-runner/manage.py","runserver","0.0.0.0:8000"]



