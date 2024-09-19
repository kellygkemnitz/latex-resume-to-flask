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
    texlive-fonts-extra \
    texlive-pictures \
    texlive-science \
    texlive-lang-cyrillic

RUN git clone https://github.com/kellygkemnitz/python-latex-resume.git

RUN cd python-latex-resume

WORKDIR /python-latex-resume

RUN python3 -m pip install -r requirements.txt

ARG NAME='Kelly Kemnitz'
ARG ROLE='qa_engineer'

CMD ['python3', 'latex_to_pdf.py', '-n', '${NAME}', '-t', '${ROLE}']

EXPOSE 80

CMD ['gunicorn', '-b', '0.0.0.0:80', '-w', '4', 'flask:app']