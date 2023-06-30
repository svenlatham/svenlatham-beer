FROM docker.io/library/python:3
WORKDIR /app/
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
# Generate thumbnails
EXPOSE 8087
ENTRYPOINT ["/bin/sh","./run.bash"]