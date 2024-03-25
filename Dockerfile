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
    wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz && \
    tar -xvf install-tl-unx.tar.gz && \
    cd install-tl-2* && \
    echo "selected_scheme scheme-full" > ./texlive.profile && \
    echo "option_doc 0" >> ./texlive.profile && \
    echo "option_src 0" >> ./texlive.profile && \
    ./install-tl -no-gui -profile ./texlive.profile && \
    /usr/local/texlive/????/bin/*/tlmgr path add && \
    cd .. && \
    rm -rf install-tl-2* && \
    apt remove -y wget && \
    apt clean -y && \
    rm -rf /var/lib/apt/lists/*

RUN apt update && \
    apt install -y default-jre graphviz && \
    apt clean -y && \
    rm -rf /var/lib/apt/lists/*