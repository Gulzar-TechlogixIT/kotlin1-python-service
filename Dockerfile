FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
COPY src/ ./src/
RUN python -m pip install --no-cache-dir .
ENV PORT=8087
EXPOSE 8087
CMD ["python", "-m", "kotlin1_python_service.server"]
