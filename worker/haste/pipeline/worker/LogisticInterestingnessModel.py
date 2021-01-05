import logging
import math


class LogisticInterestingnessModel:
    """
    Interestingness Function is the logistic function applied to an extracted feature.
    """

    def __init__(self, key, k=1, x_0=0):
        """
        :param key: path, as a list of strings, without 'metadata', to the feature used for interestingness score
        :param k: k for logistic function
        :param x_0:
        :return:
        """
        self.key = key  # list.
        self.k = k
        self.x_0 = x_0

    def interestingness(self,
                        stream_id=None,
                        timestamp=None,
                        location=None,
                        substream_id=None,
                        metadata=None,
                        mongo_collection=None):
        logging.debug('key is {}, k is {}, x_0 is {}'.format(self.key, self.k, self.x_0))

        foo = metadata
        for key_part in self.key:
            foo = foo[key_part]
        value_of_key = float(foo)

        logging.debug('extracted key value {}'.format(value_of_key))

        interestingness_score = 1 / (1 + math.exp(-self.k * (value_of_key - self.x_0)))

        logging.debug('interestingness score is {}'.format(interestingness_score))

        return {'interestingness': interestingness_score}


