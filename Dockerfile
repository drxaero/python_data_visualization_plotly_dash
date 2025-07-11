# Build image: `docker build -t py_dash:1.0 .`
# Run container: `docker run -it -p 8091:8091 --name py_dash_app py_dash:1.0`

FROM python:3-alpine

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install python packages
WORKDIR /tmp/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

# Create a directory `/app/` in the container and change the working directory to `/app/`
WORKDIR /app/

# Copy the contents of the `app/` directory to the WORKDIR in the container
COPY app/ .

# Expose port 8091
EXPOSE 8091/tcp

CMD ["./start-app"]
