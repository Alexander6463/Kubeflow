from python:3.8

RUN apt-get update && \
    apt-get install --yes locales build-essential libpoppler-cpp-dev python3-dev \
    python3-distutils poppler-utils libpoppler-qt5-1 poppler-data libleptonica-dev \
    pkg-config cmake wget curl


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /preprocess

COPY ./requirements.txt /preprocess/requirements.txt
RUN pip install -r /preprocess/requirements.txt

COPY . /preprocess

EXPOSE 8000
CMD ["/bin/bash"]