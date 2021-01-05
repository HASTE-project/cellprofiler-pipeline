import numpy as np

from haste.pipeline.worker.LogisticInterestingnessModel import LogisticInterestingnessModel

def test_LogisticInterestingnessModel():
    print('hej')

    model = LogisticInterestingnessModel(['cellprofiler_output', 'ImageQuality_PowerLogLogSlope_myimages'])

    stream_id = 'some_stream_id'
    PLLSs = np.linspace(4.5, -1.4, 100)

    assert len(PLLSs) == 100

    for plls in PLLSs:
        metadata = {
            'cellprofiler_output': {
                'ImageQuality_PowerLogLogSlope_myimages': plls
            }
        }

        result = model.interestingness(
            stream_id,
            metadata=metadata,
        )

        assert result['interestingness'] < 1
        assert result['interestingness'] > 0