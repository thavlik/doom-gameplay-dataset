FROM python3:latest
COPY requirements.txt .
RUN pip install -r requirements.txt

# TODO: install ffmpeg