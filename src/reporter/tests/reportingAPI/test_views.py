from rest_framework.test import APITestCase
from reportingAPI.views import demographic
from datetime import datetime
from unittest.mock import patch

class TestDemographic(APITestCase):
    @pytest.fixture
    def event():
        a =[{
                "eventId": 1,
                "eventName": "TestOne",
                "startDateTime": "2019-09-29T00:00:00Z",
                "endDateTime": "2019-09-28T00:00:00Z",
                "maxParticipants": 100,
                "minParticipants": 1,
                "organizerName": "test2",
                "description": "test event",
                "eventStatus": "open",
                "createdDateTime": "2019-09-28T00:00:00Z",
                "updatedDateTime": "2019-09-28T00:00:00Z"
            },
            {
                "eventId": 2,
                "eventName": "TestOne1",
                "startDateTime": "2019-09-28T00:00:00Z",
                "endDateTime": "2019-09-29T00:00:00Z",
                "maxParticipants": 100,
                "minParticipants": 1,
                "organizerName": "test2",
                "description": "test event",
                "eventStatus": "open",
                "createdDateTime": "2019-09-28T00:00:00Z",
                "updatedDateTime": "2019-09-28T00:00:00Z"
            },
        ]
        return event

    def test_aa(self):
        response = self.client.get('/reports/demographic?eventId=1')
        print(response)
        assert 1 == 2

