FROM python:3.11.10-bookworm

RUN pip install --upgrade pip

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "sh", "/entrypoint.sh" ]