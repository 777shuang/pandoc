FROM pandoc/core:latest-ubuntu
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt autoremove -y 

RUN apt update && \
    apt install -y software-properties-common && \
    add-apt-repository -y ppa:inkscape.dev/stable && \
    apt update && \
    apt install -y inkscape && \
    apt clean -y && \
    rm -rf /var/lib/apt/lists/*

RUN apt update && \
    apt install -y perl wget && \
    wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unix.tar.gz && \
    tar -xvf install-tl-unix.tar.gz && \
    cd install-tl-2* && \
    ./install-tl -no-gui && \
    /usr/local/texlive/????/bin/*/tlmgr path add && \
    cd .. && \
    rm -rf install-tl-2* && \
    apt remove -y wget && \
    apt clean -y && \
    rm -rf /var/lib/apt/lists/*

RUN apt update && \
    apt install -y wget default-jre && \
    wget -O plantuml.jar http://sourceforge.net/projects/plantuml/files/plantuml.jar/download && \
    apt remove -y wget && \
    apt clean -y && \
    rm -rf /var/lib/apt/lists/*