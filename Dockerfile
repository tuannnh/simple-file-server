FROM python:3.9

WORKDIR /app

# Expose port you want your app on
EXPOSE 8501

# Copy app code and set working directory
COPY . .

# Upgrade pip and install requirements
RUN pip install -U pip
RUN pip install -r requirements.txt

# Run
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
