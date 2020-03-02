from cortex.client import upload_sample


def test_upload_sample():
    upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
    assert True