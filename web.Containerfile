FROM python:3

ENV SHELL /bin/bash
ENV DEBIAN_FRONTEND noninteractive

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /mnt

ENTRYPOINT [ "python" ]
CMD ["main.py"]