import math
import pymongo

from pymongo import MongoClient


class NTierRankedInterestingnessModel:

    def __init__(self, key, num_tiers=4, min_docs=16):
        """
        :param key: path, as a list of strings, without 'metadata'
        :param num_tiers:
        :param min_docs:
        :return:
        """
        self.key = key  # list.
        self.key_with_metadata = ['metadata'] + self.key
        self.num_tiers = num_tiers
        self.min_docs = min_docs

    def interestingness(self,
                        stream_id=None,
                        timestamp=None,
                        location=None,
                        substream_id=None,
                        metadata=None,
                        mongo_collection=None):
        """
        :param stream_id (str): ID for the stream session - used to group all the data for that streaming session.
        :param timestamp (numeric): should come from the cloud edge (eg. microscope). integer or floating point.
            *Uniquely identifies the document within the streaming session*.
        :param location (tuple): spatial information (eg. (x,y)).
        :param substream_id (string): ID for grouping of documents in stream (eg. microscopy well ID), or 'None'.
        :param metadata (dict): extracted metadata (eg. image features).
        :param mongo_collection: collection in mongoDB allowing custom queries (this is a hack - best avoided!)
        """
        full_key_dots = '.'.join(self.key_with_metadata)
        # print(full_key_dots)

        mongo_collection.create_index([(full_key_dots, pymongo.ASCENDING)], background=True)

        num_docs = mongo_collection.count()

        if num_docs < self.min_docs:
            return {'interestingness': 1.0}

        indexes = [round(index / self.num_tiers * num_docs) for index in range(self.num_tiers - 1, 0, -1)]

        cursor = mongo_collection.find(sort=[(full_key_dots, pymongo.ASCENDING)],
                                       projection=[full_key_dots])

        # print(type(cursor))

        key_values = []

        for index in indexes:
            # a cursor can only be evaluated once.
            for doc in cursor.clone().skip(index).limit(1):
                foo = doc
                for k in self.key_with_metadata:
                    foo = foo[k]
                key_values.append(float(foo))

        foo = metadata
        for k in self.key:
            foo = foo[k]
        key_value = foo

        bools = [key_value < v for v in key_values]

        try:

            index = bools.index(True)
            # print(key_value, index)
        except ValueError as e:
            # True is not in the list.
            # its bigger than all of them.
            index = self.num_tiers - 1
        return {'interestingness': (2 * index + 1) / (2 * self.num_tiers)}


if __name__ == '__main__':
    stream_id = '2019_12_03__09_51_04_mikro-testdata-source'
    mongo_client = MongoClient('mongodb://localhost:27018/streams')
    mongo_collection = mongo_client.get_database()['strm_' + stream_id]
    print(mongo_collection.count())

    mongo_collection.delete_many({'metadata.cellprofiler_output.FileName_myimages': {'$regex': 'thumb'}})

    # db.users.findOne({"username": {$regex: ".*son.*"}});

    print(mongo_collection.count())

    model = NTierRankedInterestingnessModel(['cellprofiler_output', 'ImageQuality_PowerLogLogSlope_myimages'])

    import numpy as np

    PLLSs = np.linspace(-2.5, 0, 100)

    for plls in PLLSs:
        metadata = {
            'cellprofiler_output': {
                'ImageQuality_PowerLogLogSlope_myimages': plls
            }
        }

        result = model.interestingness(
            stream_id,
            metadata=metadata,
            mongo_collection=mongo_collection
        )
        print(result)

    # filenames = [doc['metadata']['cellprofiler_output']['FileName_myimages'] for doc in foo]
    # print(len(set(filenames)))
