import pymongo

from pymongo import MongoClient

if __name__ == '__main__':
    stream_id = '2019_12_11__11_42_24_mikro-testdata-source'
    mongo_client = MongoClient('mongodb://localhost:27018/streams')
    mongo_collection = mongo_client.get_database()['strm_' + stream_id]
    print(mongo_collection.count())

    full_key_dots = "metadata.cellprofiler_output.ImageQuality_PowerLogLogSlope_myimages"



    cursor = mongo_collection.find(sort=[(full_key_dots, pymongo.ASCENDING)],
                                   projection=[full_key_dots])

    print(list(cursor))

