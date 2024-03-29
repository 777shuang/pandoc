FROM 777shuang/pandoc

RUN apt update && \
    apt install -y --no-install-recommends python3 python3-requests && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

CMD [ "/bin/bash", "-c", "python3" ]