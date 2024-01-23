FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DOCKER_BUILDKIT=1
WORKDIR /app
COPY requirements/test.requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install -r test.requirements.txt --no-cache-dir
COPY . .
CMD ["pytest", "tests/integration_tests/test_scenario.py"]
