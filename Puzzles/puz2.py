from kivy.uix.screenmanager import Screen

from kivy.properties import ObjectProperty,ListProperty,NumericProperty,StringProperty,BooleanProperty
from functools import partial
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from random import randint
from kivy.lang import Builder 
from kivy.app import App

class Bic2(ButtonBehavior,Image):
	angle=NumericProperty(None)
	yy=NumericProperty()
	xx=NumericProperty()
	sx=NumericProperty()
	sy=NumericProperty()
	num=NumericProperty()
	def __init__(self,**kwargs):
		super(Bic2,self).__init__(**kwargs)
		self.angle=0
		self.capture=False
		self.yy=0
		self.sy=1
		self.sx=1
		
	def vib_anime(self):
		ctr=self.angle
		an=Animation(angle=(ctr-10)%360,d=.035)+Animation(angle=(ctr+10)%360,d=.035)+Animation(angle=ctr,d=.035)
		an.start(self) 
	def scl_anime(self,*args):
		an=Animation(sx=1.2,sy=1.2,d=.2)+Animation(sx=1/1.2,sy=1/1.2,d=.2)
		an.start(self)

	def vib(self,*args):
		an=Animation(yy=5,d=.1)+Animation(yy=-5,d=.2)+Animation(yy=0,d=.1)
		an.start(self) 

	def on_touch_down(self,t):
		if Puz2.ver and self.collide_point(*t.pos):
			Puz2.app.sm.get_screen('puz2').verify(self.num)
			self.vib_anime()
			self.scl_anime()
			


class Puz2(Screen):
	app=App.get_running_app()
	ver=BooleanProperty()
	def __init__(self,**kwargs):
		Builder.load_file("Puzzles/puz2.kv")
		self.back=SoundLoader.load('sound/p2/back.ogg')
		super(Puz2,self).__init__(**kwargs)
		
		# Sound:
		
		# Image:
		
		# Anima:
		# Varia:
		self.loaded=False
		self.ver=True
	def on_enter(self):
		# Sound:

		self.back.play()
		# Image:
		
		# Anima:
		self.ans=[self.ids.france,self.ids.morocco,self.ids.japan]
		self.an=[0,0,0]
		for i in range(3):
			self.ans[i].x=(.12+.26*i)*self.width
			self.ans[i].y=.35*self.height
			self.an[i]=Clock.schedule_interval(self.ans[i].vib,.5)

	def logic(self,*args):
		pass
		
	def verify(self,num,*args):
		self.ver=False
		if num in [1,2]:
			self.wilo(b=0)
		else:
			self.wilo()
		for i in range(3):
			self.an[i].cancel()
		
	def wilo(self,b=1,l=0,*args):
		if l:
			self.ids.cgr.opacity=0
			self.ids.hnt.opacity=0
			self.ids.next.opacity=0
			self.ids.next.disabled=True
			try:
				self.app.root.ids['pro'].cgr.stop()
			except:
				print('cgr sound not found to be stopped')

		else:
			if b:
				self.app.root.ids['pro'].cgr.play()
				self.ids.cgr.opacity=1
				self.ids.next.opacity=1
				self.ids.next.disabled=False

			else:
				self.ids.hnt.opacity=1
				self.app.root.ids['pro'].hnt.play()
				Clock.schedule_once(partial(self.app.change,'loose_screen'),1.5)

	def on_leave(self):
		# Sound:
		self.back.stop()
		# Image:
		self.wilo(l=1)
		# Anime:
		
		# Varia:
		self.ver=True