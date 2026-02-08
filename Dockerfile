
FROM python:3.13

RUN pip install pipenv

WORKDIR /Market-simulator

COPY Pipfile Pipfile.lock ./

RUN pipenv install --deploy --system

COPY . .

EXPOSE 8000

# CMD ["python","db_setup.py"] && ["uvicorn","main:app","--host","0.0.0.0"]

CMD python db_setup.py && python -m pytest && uvicorn main:app --host 0.0.0.0