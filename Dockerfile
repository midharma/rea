
WORKDIR /app

RUN pip3 install -U pip

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "usu"]
 
