FROM mcr.microsoft.com/devcontainers/java:21

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV TZ="Australia/Canberra"
USER vscode