FROM archlinux

RUN pacman -Syuu --noconfirm && \
    pacman -S pandoc texlive texlive-langcjk --noconfirm