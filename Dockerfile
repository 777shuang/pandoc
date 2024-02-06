FROM ubuntu
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y texlive-lang-japanese texlive-latex-extra xdvik-ja