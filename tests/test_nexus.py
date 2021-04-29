import pytest
from codes_api import *



class TestNexus():

    def test_get_nexus_outcodes(self):
        
        expected_results = 'this is going to be the expected result'
        
        result = 'this is going to be the expected result'
        
        assert result == expected_results