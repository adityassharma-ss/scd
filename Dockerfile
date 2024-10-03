# # Dockerfile
# FROM python:3.9-slim AS build

# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . /app

# # Final production image
# FROM python:3.9-slim

# WORKDIR /app
# COPY --from=build /app /app
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose Streamlit port
EXPOSE 8501

CMD ["streamlit", "run", "app/frontend.py"]
