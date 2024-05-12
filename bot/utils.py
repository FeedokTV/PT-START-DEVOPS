import logging
import re
import paramiko
import os
from dotenv import load_dotenv

load_dotenv(override=True)

def find_emails(text):
    return re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)

def find_phone_numbers(text):
    # Шаблоны для номеров телефонов
    patterns = [
        r'(?:\+7|8)[-(]?\d{3}[)-]?\s?\d{3}\s?\d{2}\s?\d{2}\b',  # 7|8(XXX)XXXXXXX, 8 XXX XXX XX XX, 8 (XXX) XXX XX XX, 8-XXX-XXX-XX-XX
        r'(?:\+7|8)\(\d{3}\)\d{7}\b',  # 7|8(XXX)XXXXXXX
        r'(?:\+7|8)\s\d{3}\s\d{3}\s\d{2}\s\d{2}\b',  # +7|8 XXX XXX XX XX
        r'(?:\+7|8)\s\(\d{3}\)\s\d{3}\s\d{2}\s\d{2}\b',  # +7|8 (XXX) XXX XX XX
        r'(?:\+7|8)-\d{3}-\d{3}-\d{2}-\d{2}\b',  # +7|8-XXX-XXX-XX-XX
    ]

    phone_numbers = []
    for pattern in patterns:
        phone_numbers.extend(re.findall(pattern, text))

    return phone_numbers

def verify_password(password):
    # Проверяем сложность пароля с помощью регулярных выражений
    pattern = (
        r'^(?=.*[A-Z])'  # Пароль должен содержать как минимум одну заглавную букву (A–Z)
        r'(?=.*[a-z])'  # Пароль должен содержать как минимум одну строчную букву (a–z)
        r'(?=.*\d)'  # Пароль должен содержать как минимум одну цифру (0–9)
        r'(?=.*[!@#$%^&*()])'  # Пароль должен содержать как минимум один специальный символ
        r'.{8,}$'  # Пароль должен содержать не менее восьми символов
    )

    return re.match(pattern, password) is not None

def run_command(command):
    host = os.environ['RM_HOST']
    port = os.environ['RM_PORT']
    username = os.environ['RM_USER']
    password = os.environ['RM_PASSWORD']

    print(os.getenv('HOST'))
    logging.info(f'Connecting SSH to {host}:{port} via user {username} password {password}')

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password, port=port)
    except Exception as e:
        logging.error('Handled exception while connecting to host')
        logging.error(str(e))
        return 'Ошибка при выполнении команды'
    try:
        stdin, stdout, stderr = client.exec_command(command)
        data = stdout.read() + stderr.read()
        data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
        return data
    except Exception as e:
        logging.error('Handled exception while executing command')
        logging.error(str(e))
        return 'Ошибка при выполнении команды'
    finally:
        client.close()