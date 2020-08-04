"""
Test the interface of Flask app, which could also be seen as the integration testing of the covid_map project
'client' is a off-line testing object from flask app
"""
import json


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


def test_hello(client):
    """Test the hello world interface, used for testing connection"""
    response = client.get("/hello")
    assert response.data == b"Hello, World!"


def test_map(client):
    """ Test China map with json request headers, return json"""
    res = client.post('/map', data=json.dumps({'start_index': 2, 'time_index': 10}), content_type='application/json')
    assert res.status_code == 200
    assert is_json(res.data)


def test_prov_map(client):
    """ Test province map with json request, return html"""
    res = client.post('/pmap', data=json.dumps({"prov_name": "湖北", "start_index": 2, "time_index": 10})
                      , content_type='application/json')
    assert res.status_code == 200


def test_news(client):
    """Test getting news with time index, return json"""
    res = client.post('/news', data=json.dumps({"start_index": 2, "time_index": 10})
                      , content_type='application/json')
    assert res.status_code == 200
    assert is_json(res.data)

