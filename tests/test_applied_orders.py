import unittest
from diplomacy import Game
from service import GameFormatter

class TestAppliedOrders(unittest.TestCase):

    def test_one(self):
        game = Game(map_name="standard")
        print(GameFormatter.previously_applied_orders(game, 'FRANCE'))

        
    # def test_two(self):
    #     self.assertTrue(True)



if __name__ == '__main__':
    unittest.main()
