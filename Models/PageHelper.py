from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.engine import ResultProxy

class PageHelper:
    def __init__(self, query, page_params):
        self.query = query
        self.page_params = page_params
        self.session = Session()

    def count(self):
        return self.query.count()

    def get_page(self):
        page_number = self.page_params.get('pageNumber', 1)
        page_size = self.page_params.get('pageSize', 10)
        offset = (page_number - 1) * page_size
        return self.query.limit(page_size).offset(offset).all()

    def process_parameter_object(self, parameter_object):
        # Process parameters if needed, this is a placeholder
        return parameter_object

    def get_page_sql(self, sql, page_params):
        page_number = page_params.get('pageNumber', 1)
        page_size = page_params.get('pageSize', 10)
        offset = (page_number - 1) * page_size
        page_sql = text(sql).limit(page_size).offset(offset)
        return page_sql

    def execute_page_sql(self, page_sql, parameters=None):
        result: ResultProxy = self.session.execute(page_sql, parameters)
        return result.fetchall()
