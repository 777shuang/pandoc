FROM 777shuang/pandoc

RUN apt update && \
    apt install -y --no-install-recommends python python-is-python3 python3-requests && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*