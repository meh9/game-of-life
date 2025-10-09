FROM mcr.microsoft.com/devcontainers/java:21

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    . /usr/local/share/nvm/nvm.sh && \
    nvm install --lts --latest-npm --default

ENV TZ="Australia/Canberra"
USER vscode