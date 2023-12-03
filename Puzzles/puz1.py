from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty,ListProperty,NumericProperty,StringProperty
from functools import partial
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from random import randint
from kivy.lang import Builder 
from kivy.app import App

class Bic1(ButtonBehavior,Image):
	angle=NumericProperty(None)
	def __init__(self,**kwargs):
		super(Bic1,self).__init__(**kwargs)
		self.angle=0
		self.capture=False
	def on_press(self,*args):
		self.vib_anime()
	def vib_anime(self):
		ctr=self.angle
		an=Animation(angle=(ctr-10)%360,d=.035)+Animation(angle=(ctr+10)%360,d=.035)+Animation(angle=ctr,d=.035)
		for i in range(5):
			an+=an
		an.start(self) 
	def scl_anime(self,*args):
		an=Animation(size_fi_x=4,size_fi_y=4,d=1)+Animation(d=3)+Animation(size_fi_x=1,size_fi_y=1,d=1)
		an.start(self)
	def on_touch_down(self,t):
		if self.collide_point(*t.pos):
			self.capture=True
	def on_touch_up(self,t):
		self.capture=False
	def on_touch_move(self,t):
		if self.capture:
			self.center=t.pos


class Sugar(Image):
	coord=ListProperty()
	def __init__(self,**kwargs):
		super(Sugar,self).__init__(**kwargs)
		self.coord=[1,1]

class Puz1(Screen):
	def __init__(self,**kwargs):
		Builder.load_file('Puzzles/puz1.kv')
		self.back=SoundLoader.load('sound/p1/back.ogg')
		super(Puz1,self).__init__(**kwargs)
		
		self.app=App.get_running_app()
		
		# Sound:
	
		
		# Image:
		# Anima:
		# Varia:
		self.posi=[]
	
	def on_enter(self):
		# Sound:
		self.back.play()
		# Image:
		self.cup=self.ids.cu
		self.cup.center=(self.width/2.0,self.height/2.5)
		self.sug=self.ids.su
		# Anima:
		self.an=Clock.schedule_interval(self.logic,.05)
		self.vr=Clock.schedule_interval(self.verify,.5)
		#Clock.schedule_once(partial(self.app.change,"puz2"),5)

	def logic(self,*args):
		self.sug.center=(self.cup.center[0],self.cup.center[1]-self.cup.height/3.5)
		
	def verify(self,*args):
		self.posi.append(self.sug.pos[0])
		if self.sug.opacity<0.1:
			self.wilo()
			self.vr.cancel()
		elif len(self.posi)>3:
			x,y,z=self.posi[-3:]
			if (y<x and y<z) or (y>x and y>z):
				self.sug.opacity-=0.15

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
		if self.back!='':
			self.back.stop()
		# Image:
		self.wilo(l=1)
		# Anime:
		self.an.cancel()
		self.vr.cancel()
		# Varia:
		self.posi=[]
		self.sug.opacity=.4