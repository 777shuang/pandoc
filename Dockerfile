FROM ubuntu
ENV DEBIAN_FRONTEND=noninteractive
RUN add-apt-repository -y ppa:inkscape.dev/stable && \
    apt update && \
    apt upgrade -y && \
    apt install -y texlive-lang-japanese texlive-latex-extra xdvik-ja inkscape