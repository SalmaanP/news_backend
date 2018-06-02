FROM continuumio/miniconda

RUN conda update conda

RUN conda install numpy scipy scikit-learn

WORKDIR /usr/share/news_backend
COPY ./ ./

RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/bash"]