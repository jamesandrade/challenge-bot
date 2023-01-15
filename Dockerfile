FROM python:3.10.6-slim-bullseye
WORKDIR /bot
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . /bot
EXPOSE 5000
RUN pip install -r requirements.txt
RUN python -m playwright install
RUN python -m playwright install-deps
CMD ["python", "app.py"]
