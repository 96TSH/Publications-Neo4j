# Build the Django backend
FROM python:3.9.19
WORKDIR /app
COPY Backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
COPY Backend/ ./

# Expose port 8000 for the application
EXPOSE 8000

# Start the application
CMD ["gunicorn", "neopub.wsgi:application", "--bind", "0.0.0.0:8000"]