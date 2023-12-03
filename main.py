from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty

#from kivmob import KivMob
import importlib

from kivy.core.window import Window
from kivy.utils import platform
if platform not in ("android", "ios"):
    #Window.size = (1280, 720)
    Window.size = (1920, 1080)

class mainapp(MDApp):
	sm=ObjectProperty()
	pro=ObjectProperty()

	def build(self):
		self.ads=None
		self.sm=self.root.ids['sm']
		self.pro=self.root.ids.pro
		self.theme_cls.theme_style='Dark'
		self.puz={i:self.get_sc for i in range(1,10)}
		self.load=8
		self.lo=False
		self.inter=1
		

		
	def change(self,name,*args):
		"""
		if self.ads==None:	
			self.ads = KivMob("ca-app-pub-8601014014981681~7747614968")
			self.ads.new_interstitial("ca-app-pub-8601014014981681/3758013466")
			self.ads.request_interstitial()
			self.ads.new_banner("ca-app-pub-8601014014981681/3101792948", top_pos=False)
			self.ads.request_banner()
			self.ads.show_banner()
		if self.inter==3:
			self.inter=1
			self.ads.show_interstitial()
			self.ads.request_interstitial()
		elif self.inter==2:
			self.ads.request_banner()
			self.ads.show_banner()
			self.inter+=1
		else:
			self.inter+=1
		"""

		if name not in ['welcome_screen','loose_screen','win_screen']:
			self.pro.op=1
			xx=int(name[-1])
			self.pro.score(xx)
			

			if xx==self.load:
				self.puz[xx](xx)
				self.load+=1

			if xx==2 and not self.lo:
				self.get_scs('lo')
				self.lo=True


		else:
			if name=='win_screen':self.get_scs('wi')

			self.pro.op=1
		if self.lo:
			self.sm.get_screen('loose_screen').last_session=self.sm.current
		self.sm.current=name
		if name=='loose_screen':
			self.sm.get_screen('loose_screen').life_score-=1
		if name=='welcome_screen':
			self.sm.get_screen('loose_screen').life_score=3


	def get_sc(self,x):
		mod=importlib.import_module('Puzzles.puz'+str(x))
		puz=getattr(mod,'Puz'+str(x))
		self.sm.add_widget(puz(name='puz'+str(x)))
	def get_scs(self,name):
		mod=importlib.import_module(name)
		az='LooseScreen' if name=='lo' else 'WinScreen'
		azz='loose_screen' if name=='lo' else 'win_screen'
		puz=getattr(mod,az)
		self.sm.add_widget(puz(name=azz))


mainapp().run()