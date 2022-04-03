# Define your item pipelines here
import logging
import psycopg2
from psycopg2.extensions import AsIs
from scrapy.utils.project import get_project_settings


class PostgresqlPipeline(object):

    def open_spider(self, spider):
        settings = get_project_settings()
        username = settings['USERNAME']
        password = settings['PASSWORD']
        hostname = settings['HOSTNAME']
        port = settings['PORT']
        database = settings['DATABASE']
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=port)
        self.cur = self.connection.cursor()
        self.cur.execute('delete from bikez_database')
        self.connection.commit()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        columns = item.keys()
        values = [item[column] for column in columns]
        insert_statement = f'insert into bikez_database (%s) values %s'
        try:
            self.cur.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
            self.connection.commit()
            logging.debug("inserted into database")
        except psycopg2.InternalError as e:
            self.connection.rollback()
            logging.debug(e)

        return item
