FROM python:3.10

WORKDIR /app

EXPOSE 22

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN rm -rf /root/.ssh/known_hosts


CMD python bot.py
