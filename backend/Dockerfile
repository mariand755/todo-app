FROM python:3.13
RUN pip install uv
WORKDIR /app
COPY . .
RUN uv sync
CMD ["uv", "run", "fastapi", "dev", "fastapi_tool/fastapi.py", "--port", "8000", "--host", "0.0.0.0"]