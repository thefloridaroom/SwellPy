import unittest
from ParticleSuspension import *

class TestParticleSuspension(unittest.TestCase):


    def test_randomCentersShape(self):
        x = ParticleSuspension(10, 0.2)
        self.assertEqual(x.centers.shape, (10, 2))

    def test_randomCentersBounds(self):
        x = ParticleSuspension(10, 0.2)
        self.assertTrue( (x.centers > 0).all() )
        self.assertTrue( (x.centers < x.boxsize).all() )

    def test_setBadFormatCenters(self):
        x = ParticleSuspension(3, 0.2)
        before = x.centers
        x.setCenters([0,2,3,4,4,5,6]) # Attempt bad center reassignment (message will print)
        after = x.centers
        self.assertTrue( before is after )

    def test_setOutOfBoundsCenters(self):
        x = ParticleSuspension(2, 0.2)
        x.setCenters([[0,1],[-10,12]])
        self.assertTrue( (x.centers == [[0,1],[-10,12]]).all() ) # Out of bounds reassignment (message will print)

    def test_setCenters(self):
        x = ParticleSuspension(2, 0.2)
        new = [[0,1],[2.0, 1.89]]
        x.setCenters(new)
        self.assertTrue( (x.centers == new).all() )

    def test_reset(self):
        x = ParticleSuspension(10, 0.2, 10) # Feeding seed for randomization
        before = x.centers
        x.reset(10) # feeding same seed
        after = x.centers
        self.assertTrue( (before == after).all() ) 

    def test_direcTag(self):
        x = ParticleSuspension(2, 0.2)
        x.setCenters([[1,1], [1,1.5]])
        tagged = x.tag(1.0)
        self.assertTrue( (tagged == [[0,1]]).all() ) 

    def test_boundaryTag(self):
        x = ParticleSuspension(2, 0.2)
        x.setCenters([[0,0],[0, 2]])
        tagged = x.tag(1.0)
        self.assertTrue( (tagged == [[0,1]]).all() ) 

    def test_wrap(self):
        x = ParticleSuspension(2, 0.2)
        x.setCenters([[-1, 0], [0, 1]]) # Will print warning message
        x.wrap()
        self.assertTrue( (x.centers == [[x.boxsize-1, 0], [0,1]]).all() )

    def test_normalRepel(self):
        x = ParticleSuspension(2, 0.1)
        x.setCenters([[1,1],[1.5,1.5]])
        before = x.centers
        x.repel(np.array([[0,1]]), 1.0, 1.0)
        after = x.centers
        self.assertEqual( (before-after)[0][0], (before-after)[0][1] )
        self.assertEqual( (before-after)[1][0], (before-after)[1][1] )
        self.assertEqual( (before-after)[0][0], -(before-after)[1][0] )
        self.assertEqual( (before-after)[0][1], -(before-after)[1][1] )

    def test_boundaryRepel(self):
        x = ParticleSuspension(2, 0.1)
        x.setCenters([[0,0],[0, 2]])
        before = x.centers
        x.repel([[0,1]], 1.0, 1.0)
        after = x.centers
        self.assertEqual( before[0][1], after[0][1] )
        self.assertEqual( before[1][1], after[1][1] )
        self.assertEqual( (before-after)[0][0], -(before-after)[1][0] )

    def test_train(self):
        x = ParticleSuspension(2, 0.1)
        before = [[1, 0],[1.25, 0]]
        x.setCenters(before)
        x.train(1.0, 0.1)
        after = x.centers
        self.assertEqual( before[0][1], after[0][1] )
        self.assertEqual( before[1][1], after[1][1] ) 
        self.assertTrue( abs(after[1,0] - after[1][1]) > 1.0 )

    def test_fracTagAt(self):
        x = ParticleSuspension(2, 0.2)
        x.setCenters([[0,1],[0, 1.25]])
        self.assertEqual(x.fracTagAt(1.0), 1.0)
        self.assertEqual(x.fracTagAt(0.24), 0)

    def test_fracTag(self):
        x = ParticleSuspension(3, 0.2)
        x.setCenters([[0,1],[0, 1.25], [0, 0.25]])
        (swell, tagged) = x.fracTag(0, 1.0, 0.2)
        self.assertTrue( (tagged == [0.0, 0.0, 2.0/3, 2.0/3, 1.0, 1.0]).all() )
        self.assertTrue( np.allclose(swell, [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]) )

    def test_fracTagNegative(self):
        x = ParticleSuspension(3, 0.2)
        x.setCenters([[0,1],[0, 1.25], [0, 0.25]])
        (swell, tagged) = x.fracTag(0, -1.0, -0.2)
        self.assertTrue( (tagged == [0.0, 0.0, 2.0/3, 2.0/3, 1.0, 1.0]).all() )

    def test_tagRate(self):
        x = ParticleSuspension(3, 0.2)
        x.setCenters([[0,1],[0, 1.25], [0, 0.25]])
        (swells, rate) = x.tagRate(0, 1.0, 0.2)
        self.assertTrue( np.allclose(rate, [0, (2.0/3)/0.2, 0, 0, (1-2/3)/0.2, 0]) )

    def test_tagCurve(self):
        x = ParticleSuspension(3, 0.2)
        x.setCenters([[0,1],[0, 1.25], [0, 0.25]])
        (swells, curve) = x.tagCurvature(0, 1.0, 0.2)
        self.assertTrue( np.allclose(curve, [0, (2.0/3)/0.04, -(2.0/3)/0.04, (1/3)/0.04, -(1/3)/0.04, 0]) )


if __name__ == "__main__":
    unittest.main()