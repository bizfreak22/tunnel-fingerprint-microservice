FROM python:3.7-alpine
RUN pip install pipenv gunicorn
WORKDIR /app
COPY . .
RUN pipenv install --system --deploy --ignore-pipfile
EXPOSE 80
CMD ["gunicorn", "-b", "0.0.0.0:80", "main:app"]
