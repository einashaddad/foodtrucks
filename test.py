from foodtrucks import *
import pytest

def test_geocode_location():
    """ Test that geocoding an address works
    """
    #ensure that function returns None on invalid address
    address = 'This is my fake address'
    assert geocode_location(address) == None

    #ensure that only valid addresses in San Francisco are returned
    address = '159 Varick St, New York'
    assert geocode_location(address) == None

    #ensure that function works for valid address
    address = '182 howard st, san francisco'
    assert geocode_location(address) != None

def test_calculate_bounds():
    # make sure calculations are working correctly
    user_location = (0, 0)
    bounds = calculate_bounds(user_location, 69)
    assert bounds[0] == (1, -1)
    assert bounds[1] == (-1, 1)

def test_get_foodtrucks():
    # make sure API call is working correctly
    user_location = (37.7908906, -122.3930944) 
    northwest = (37.79813697681159, -122.40037140364292) 
    southeast = (37.7836442231884, -122.38581739635707)
    foodtrucks = get_foodtrucks(user_location, (northwest, southeast))
    assert type(foodtrucks) == list

    # make sure no trucks still returns a list
    user_location = (0,0)
    northwest = (0,0)
    southeast = (0,0)
    foodtrucks = get_foodtrucks(user_location, (northwest, southeast))
    assert type(foodtrucks) == list

def test_remove_duplicates():
    # make sure removes duplicates accoring to applicant name
    user_location = (37.768277, -122.431616)
    list_of_trucks = [  {'applicant': "Katie's Catering", 'longitude': '-122.427110643955', 'latitude': '37.7683202495106'},
                        {'applicant': "Daniel's Catering", 'longitude': '-122.427110643955', 'latitude': '37.7683202495106'},
                        {'applicant': "Daniel's Catering", 'longitude': '-122.429511176347', 'latitude': '37.7666247727157'} ]
    list_of_trucks = remove_duplicates(list_of_trucks, user_location)
    assert len(list_of_trucks) == 2

    # make sure returns a list at invalid input
    user_location = (0,0)
    list_of_trucks = []
    list_of_trucks = remove_duplicates(list_of_trucks, user_location)
    assert type(list_of_trucks) == list

def test_distance():
    loc1 = (0, 3)
    loc2 = (4, 0)
    assert distance(loc1, loc2) == 5

