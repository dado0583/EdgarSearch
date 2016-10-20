FROM python

RUN pip install pymongo
RUN pip install bs4

COPY . /
CMD ["python", "./filings/FilingSeacher.py"]
