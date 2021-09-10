FROM python:3

WORKDIR /usr/src/app

COPY requirement.txt ./
RUN pip install --no-cache-dir -r requirement.txt

ENV WALLET_ADDRESS 0x
ENV INFURA_API_KEY ''
ENV TARGET_GEM 1
ENV NOTIFY_AUTH_TOKEN ''

COPY . .

CMD [ "python", "./auto_mine.py" ]
