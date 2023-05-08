FROM python:3.7-slim

COPY . /streamlit
WORKDIR /streamlit

RUN pip install -r requirements.txt

EXPOSE 8501

# CMD ["streamlit", "run", "test.py", "--server.port", "8501"]