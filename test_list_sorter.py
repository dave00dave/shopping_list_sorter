import pytest
from list_sorter import *

# Define fixtures to provide mock inputs to test
@pytest.fixture
def store_items():
    return ['Fruit', 'Bread', 'Ice Cream', 'Peppers, Green']

# def test_add_1():
#     i = item('test_item', False)
#     i.add_1()
#     assert(i.quant == 1)

def test_check_item_wo_numbers(store_items):
    """Test identifying an item from the store that has (#)

    Pass an item that is in the store's list and make sure
    we get the item back without the (#) at the end.
    """

    i = store_items[0] + ' (2)'
    res = check_without_number(i, store_items)
    assert(res == store_items[0])

def test_check_no_item_wo_numbers(store_items):
    """Test checking for an item with (#) that should not return any item

    Pass an item that is in the store's list and make sure
    we get the item back without the (#) at the end.
    """

    i = ' '
    res = check_without_number(i, store_items)
    assert(res == '')