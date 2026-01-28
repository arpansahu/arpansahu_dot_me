FROM python:3.10.7

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

EXPOSE 8000

CMD bash -c "python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 arpansahu_dot_me.wsgi"