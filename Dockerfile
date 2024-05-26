# Choose base image
FROM python:3.11

# Create dir
WORKDIR /URL-Shortener

# Install dependencies
COPY ./requirements.txt /URL-Shortener/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /URL-Shortener/requirements.txt

# Copy necessary files
COPY . /URL-Shortener/


# Run tests first, then start server
CMD ["/bin/bash","-c","pytest -v; uvicorn app.main:app --reload --host 0.0.0.0 --port 80"]