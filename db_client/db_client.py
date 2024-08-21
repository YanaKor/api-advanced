import uuid

import records
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4,
                                          ensure_ascii=True,
                                          # sort_keys=True
                                          )
    ]
)


class DbClient:

    def __init__(self, user, password, host, database):
        connection_string = f'postgresql://{user}:{password}@{host}/{database}'
        # 'postgresql://postgres:admin@5.63.153.31/dm3.5'
        self.db = records.Database(connection_string)
        self.log = structlog.getLogger(self.__class__.__name__).bind(service='db')

    def send_query(self, query):
        print(query)
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event='request',
            query=query
        )
        dataset = self.db.query(query=query).as_dict()
        log.msg(
            event='response',
            dataset=dataset
        )
        return dataset
