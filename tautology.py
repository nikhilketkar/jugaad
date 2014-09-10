import sys
import itertools
import unittest

def isTautology(statement):
    symbols = list(set(statement.replace("!", "").replace("&", "").replace("|", "").replace("(","").replace(")","").replace("  "," ").split()))
    tautology = True
    for symbolValues in itertools.product(*[[True, False]] * len(symbols)):
        for symbol, value in zip(symbols, symbolValues):
            exec(symbol + " = " + str(value))
        if not eval(statement.replace("!", "not ").replace("&", "and ").replace("|", "or ")):
            tautology = False
            break
    return tautology

class TestTautology(unittest.TestCase):
    def test_cases(self):
        self.assertFalse(isTautology('a'))
        self.assertFalse(isTautology('a & b'))
        self.assertFalse(isTautology('a & (b | c)'))
        self.assertFalse(isTautology('!a & !b'))
        self.assertTrue(isTautology('a | !a'))
        self.assertTrue(isTautology('(a & (!b | b)) | (!a & (!b | b))'))

if __name__ == '__main__':
    unittest.main()
