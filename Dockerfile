FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Expose port you want your app on
EXPOSE 8585

# Copy app code and set working directory
COPY . .

# Upgrade pip and install requirements
RUN pip install -U pip
RUN pip install -r requirements.txt

# Run
ENTRYPOINT ["streamlit", "run", "app.py"]
