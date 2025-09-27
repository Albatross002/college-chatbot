FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV GEMINI_API_KEY=AIzaSyCF-nwmq7XFWKh9lNlfooTqCaVqUXE8YhU
ENV CARGO_HOME=/app/.cargo
ENV PATH="$CARGO_HOME/bin:$PATH"

# Install build tools (for any packages that might need compilation)
RUN apt-get update && apt-get install -y curl build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
