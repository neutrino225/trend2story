FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .
RUN conda env create -f environment.yml

RUN apt-get update && \
    apt-get install -y chromium chromium-driver fonts-liberation libnss3 libatk-bridge2.0-0 libgtk-3-0 libxss1 libasound2 libgbm1 && \
    rm -rf /var/lib/apt/lists/*

COPY . .

ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="${CHROME_BIN}:${PATH}"

EXPOSE 50051

# Add entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
