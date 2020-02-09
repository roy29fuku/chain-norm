import unittest
from cnorm.rule import Word2Num, RomNum2AraNum


class Word2NumTest(unittest.TestCase):
    rule = Word2Num()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_1(self):
        text = 'one hundred apples.'
        answer = '100 apples.'
        self.assertEqual(answer, self.rule.apply(text))

    def test_2(self):
        text = 'one hundred apples two million oranges.'
        answer = '100 apples 2000000 oranges.'
        self.assertEqual(answer, self.rule.apply(text))

    def test_3(self):
        text = 'type four'
        answer = 'type 4'
        self.assertEqual(answer, self.rule.apply(text))


class RomNum2AraNumTest(unittest.TestCase):
    rule = RomNum2AraNum()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_1(self):
        text = 'Glycogen storage disease type Ⅳ'
        answer = 'Glycogen storage disease type four'
        self.assertEqual(answer, self.rule.apply(text))


if __name__ == "__main__":
    unittest.main()
