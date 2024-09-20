FROM alpine

RUN apk update && apk add \
    python3 \
    git \
    py3-pip \
    texlive-full

RUN git clone https://github.com/kellygkemnitz/python-latex-resume.git

RUN cd python-latex-resume

WORKDIR /python-latex-resume

RUN python3 -m venv venv

RUN source venv/bin/activate

RUN python3 -m pip install -r requirements.txt

ARG name='Kelly Kemnitz'
ARG role='qa_engineer'

EXPOSE 80

RUN python3 latex_to_pdf.py -n $name -t $role

CMD ["gunicorn", "-b", "0.0.0.0:80", "-w", "4", "flask_app:app"]