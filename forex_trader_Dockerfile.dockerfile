FROM python:3.10-windowsservercore

# Install MT4 via Chocolatey
RUN powershell -Command \
    Set-ExecutionPolicy Bypass -Scope Process -Force; \
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; \
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1')); \
    choco install metatrader4 -y

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]