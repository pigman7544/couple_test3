import unittest
from pathlib import Path
from server import compute
from story_report import ten_god

SAMPLE={'a':{'date':'1992-03-18','time':'16:00','calendar':'solar'},'b':{'date':'1992-04-30','time':'01:00','calendar':'solar'}}
class V5Tests(unittest.TestCase):
    def test_real_match(self):
        d=compute(SAMPLE)
        self.assertEqual(d['couple']['id'],'c06')
        self.assertTrue(d['has_art'])
    def test_determinism(self):self.assertEqual(compute(SAMPLE),compute(SAMPLE))
    def test_longform(self):
        r=compute(SAMPLE)['full_report']
        self.assertGreater(sum(len(r[k]) for k in ('story','saju_a','saju_b','chemistry','roles','scene','tip')),5000)
        self.assertIn('월간',r['saju_a'])
        self.assertIn('육합',r['chemistry']) if '육합' in r['chemistry'] else self.assertIn('지지',r['chemistry'])
    def test_assets(self):
        for n in ('baek_heo_title.png','baek_heo_plain.png'):
            f=Path(__file__).parent/'assets'/n
            self.assertTrue(f.exists())
            self.assertGreater(f.stat().st_size,100000)
    def test_tengods(self):
        self.assertEqual(ten_god('甲','甲'),'비견')
        self.assertEqual(ten_god('甲','乙'),'겁재')
        self.assertEqual(ten_god('甲','丙'),'식신')
        self.assertEqual(ten_god('甲','丁'),'상관')
        self.assertEqual(ten_god('甲','戊'),'편재')
        self.assertEqual(ten_god('甲','己'),'정재')
        self.assertEqual(ten_god('甲','庚'),'편관')
        self.assertEqual(ten_god('甲','辛'),'정관')
        self.assertEqual(ten_god('甲','壬'),'편인')
        self.assertEqual(ten_god('甲','癸'),'정인')
if __name__=='__main__':unittest.main()
