FROM python

RUN pip install pymongo
RUN pip install bs4

COPY . /

CMD ["python3", "./filings/FilingSearcher.py"]
