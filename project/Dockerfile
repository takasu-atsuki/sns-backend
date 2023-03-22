FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python3 -m pip install --upgrade pip setuptools
RUN pip3 install -r requirements.txt

COPY . ./

# RUN mkdir -p /var/run/gunicorn

# CMD ["gunicorn", "sns.wsgi", "--bind=unix:/var/run/gunicorn/gunicorn.sock"]

CMD ["gunicorn", "--bind",  ":8000", "sns.wsgi:application"]

EXPOSE 8000