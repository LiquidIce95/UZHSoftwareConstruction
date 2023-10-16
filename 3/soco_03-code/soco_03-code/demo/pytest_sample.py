import func

def test_add_one_happy():
  assert func.add_one(3) == 4

def test_add_one_wrong():
  assert func.add_one(4) == 5

