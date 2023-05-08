FROM python:3.9-slim-buster

COPY . /src
WORKDIR /src

RUN apt-get update && apt-get install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1
RUN pip install --no-cache-dir --upgrade  -r requirements.txt

EXPOSE 8090

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]