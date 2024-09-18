FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt-get update && apt-get install -y \
    python3-pip \
    git \
    latexmk \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    # texlive-pictures \
    # texlive-science \
    texlive-lang-cyrillic

RUN git clone https://github.com/kellygkemnitz/python-latex-resume.git

RUN cd python-latex-resume

WORKDIR /python-latex-resume

# FROM python:3.12-slim
# WORKDIR /python-latex-resume
# ADD python-latex-resume /python-latex-resume/
# WORKDIR /python-latex-resume
# WORKDIR /python-latex-resume
# COPY python-latex-resume.py requirements.txt README.md /python-latex-resume/
# COPY templates/ /python-latex-resume/
# COPY resumes/ /python-latex-resume/

RUN python3 -m pip install -r requirements.txt
