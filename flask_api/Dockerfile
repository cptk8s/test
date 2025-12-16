FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV DATABASE_URI="sqlite:///data.db"
EXPOSE 5000
CMD ["python","run.py"]
