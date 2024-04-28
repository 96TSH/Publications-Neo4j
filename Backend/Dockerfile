# Build the Django backend
FROM python:3.9.19
WORKDIR /usr/src/app
COPY Backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY Backend/ ./

# Expose port 8000 for the application
EXPOSE 8000

# Start the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]