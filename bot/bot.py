import asyncio
import logging
import os
from misc import bot,dp
from messages.register_handlers import register_messages_handlers
import subprocess

async def run_ssh_server():
    # Обновление списка пакетов и установка openssh-server
    subprocess.run(["apt-get", "update"])
    subprocess.run(["apt-get", "install", "-y", "openssh-server", "sudo"])

    # Создание директорий
    subprocess.run(["mkdir", "-p", "/root/.ssh"])
    subprocess.run(["mkdir", "/var/run/sshd"])
    subprocess.run(["chmod", "0755", "/var/run/sshd"])

    subprocess.run(["useradd", "-p", os.environ['RM_PASSWORD'], os.environ['RM_USER']])
    subprocess.run(["usermod", "-G", "root", os.environ['RM_USER']])
    subprocess.run(["mkdir", f"/home/{os.environ['RM_USER']}"])
    subprocess.run(["chown", f"{os.environ['RM_USER']}:{os.environ['RM_USER']}", f"/home/{os.environ['RM_USER']}"])
    cmd = f"echo '{os.environ['RM_USER']}:{os.environ['RM_PASSWORD']}' | chpasswd"
    subprocess.run(cmd, capture_output=True, shell=True)
    subprocess.run(["adduser", os.environ['RM_USER'], "sudo"])

    # Запуск SSH-сервера
    subprocess.run(["/usr/sbin/sshd"])

async def main():
    logging.info('Starting SSH server')
    await run_ssh_server()
    register_messages_handlers(dp)
    logging.info('Starting bot')

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
