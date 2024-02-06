FROM pandoc/core
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y software-properties-common && \
    add-apt-repository -y ppa:inkscape.dev/stable && \
    apt update && \
    apt install -y texlive-lang-japanese texlive-latex-extra xdvik-ja inkscape