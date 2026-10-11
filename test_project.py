import pytest

from project import Aircraft, find_plane, check_win, check_donger

###### FIND PLANE ########################

def test_find_plane():
    plane1 = Aircraft()
    plane2 = Aircraft()
    plane1.codename = 'AB12'
    plane2.codename = 'CD34'
    planes = [plane1, plane2]
    assert find_plane(planes, 'AB12') is plane1
    assert find_plane(planes, 'CD34') is plane2

def test_find_plane_not_found():
    plane = Aircraft()
    plane.codename = 'AB12'
    planes = [plane]
    assert find_plane(planes, 'ZZ99') is None

###### CAN LAND ########################

def test_can_land():
    plane = Aircraft()
    plane.distance = 0
    assert plane.can_land() is True

def test_cannot_land():
    plane = Aircraft()
    plane.distance = 1
    assert plane.can_land() is False
    plane.distance = -1
    assert plane.can_land() is False

###### MOVE ########################

def test_move_inbound():
    plane = Aircraft()
    plane.distance = 5
    plane.speed = 2
    plane.fuel = 10
    plane.holding = False
    plane.direction = -1
    plane.move()
    assert plane.distance == 3
    assert plane.fuel == 9

def test_move_crosses_zero_inbound():
    plane = Aircraft()
    plane.distance = 2
    plane.speed = 3
    plane.fuel = 10
    plane.holding = False
    plane.direction = -1
    plane.move()
    assert plane.distance == 0
    assert plane.fuel == 9
    assert plane.direction == -1
    plane.move()
    assert plane.distance == -3
    assert plane.fuel == 8
    assert plane.direction == -1

def test_move_returning():
    plane = Aircraft()
    plane.distance = -5
    plane.speed = 2
    plane.fuel = 10
    plane.holding = False
    plane.direction = 1
    plane.move()
    assert plane.distance == -3
    assert plane.fuel == 9

def test_move_crosses_zero_returning():
    plane = Aircraft()
    plane.distance = -2
    plane.speed = 3
    plane.fuel = 10
    plane.holding = False
    plane.direction = 1
    plane.move()
    assert plane.distance == 0
    assert plane.fuel == 9
    assert plane.direction == 1
    plane.move()
    assert plane.distance == 3
    assert plane.fuel == 8
    assert plane.direction == 1

###### HOLDING ########################

def test_move_holding():
    plane = Aircraft()
    plane.distance = 5
    plane.speed = 2
    plane.fuel = 10
    plane.holding = True
    plane.move()
    assert plane.distance == 5
    assert plane.fuel == 9

###### WIN CONDITION ########################

def test_check_win_does_not_exit():
    check_win(9)

def test_check_win():
    with pytest.raises(SystemExit):
        check_win(10)

def test_check_win_above_limit():
    with pytest.raises(SystemExit):
        check_win(15)

###### DANGER CHECK ########################

def test_check_donger():
    plane = Aircraft()
    plane.fuel = 0
    plane.distance = 5
    with pytest.raises(SystemExit):
        check_donger([plane])

def test_collision_game_over():
    plane1 = Aircraft()
    plane2 = Aircraft()
    plane1.distance = 5
    plane2.distance = 5
    plane1.fuel = 10
    plane2.fuel = 10
    with pytest.raises(SystemExit):
        check_donger([plane1, plane2])

###### FUEL ########################

def test_aircraft_fuel():
    plane = Aircraft()
    while plane.distance > 0:
        plane.move()
    assert plane.can_land() is True
    assert plane.fuel > 0

def test_check_donger_safe():
    plane1 = Aircraft()
    plane2 = Aircraft()
    plane1.distance = 4
    plane2.distance = 5
    plane1.fuel = 10
    plane2.fuel = 10
    assert check_donger([plane1,plane2]) is None
