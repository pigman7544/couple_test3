import unittest
from server import compute
from astrology import sun_profile, apply_sun_signs
from pathlib import Path
S={'a':{'date':'1992-03-18','time':'16:00','calendar':'solar'},'b':{'date':'1992-04-30','time':'01:00','calendar':'solar'}}
class V6(unittest.TestCase):
 def test_astro(self):
  d=compute(S);r=d['full_report'];self.assertIn('물고기자리',r['astrology']);self.assertIn('황소자리',r['astrology'])
 def test_repeat(self):self.assertEqual(compute(S),compute(S))
 def test_swap(self):
  d=compute(S);sw={'a':S['b'],'b':S['a']};self.assertEqual(d['couple']['id'],compute(sw)['couple']['id'])
 def test_mbti(self):
  s={'a':dict(S['a'],mbti='ENFP'),'b':dict(S['b'],mbti='ISTJ')};self.assertIn('ENFP',compute(s)['full_report']['mbti_note'])
 def test_no_time(self):
  s={'a':dict(S['a'],time=''),'b':dict(S['b'],time='')};self.assertTrue(compute(s)['full_report']['story'])
 def test_images(self):
  from PIL import Image
  
  with Image.open('assets/baek_heo_plain.png') as a, Image.open('assets/baek_heo_title.png') as b:self.assertEqual(a.size,b.size)
 def test_html(self):
  s=Path('index.html').read_text();self.assertIn('id="astroText"',s);self.assertIn('id="artSection"',s);self.assertIn('MBTI',s)
if __name__=='__main__':unittest.main()
