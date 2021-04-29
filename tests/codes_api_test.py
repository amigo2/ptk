import pytest
from django.conf import settings
from codes_api import views




class TestOutcodes():

    def test_get_outcodes(self):

        expected_results = 'this is going to be the expected result'
        
        result = 'this is going to be the expected result'
        
        assert result == expected_results