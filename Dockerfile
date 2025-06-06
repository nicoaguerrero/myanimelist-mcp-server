# Generated by https://smithery.ai. See: https://smithery.ai/docs/build/project-config
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml main.py uv.lock README.md LICENSE /app/
COPY tools /app/tools
COPY utils /app/utils

# Install dependencies
RUN pip install --no-cache-dir .

# Default command for stdio transport
CMD ["python", "main.py"]
