FROM apache/airflow:2.1.0
# this fixes a warning in the official image, with the Azure provider
# More info here https://github.com/apache/airflow/issues/14266#issuecomment-786298240
RUN pip3 install Scrapy
RUN pip3 install pymongo
# add your dependencies here:
# RUN pip install package1 package2....