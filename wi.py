from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty,ListProperty,NumericProperty,StringProperty
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.lang import Builder 
from random import randint

class Bicwin(ButtonBehavior,Image):
	angle=NumericProperty(None)
	def __init__(self,**kwargs):
		super(Bicwin,self).__init__(**kwargs)
		self.angle=0
		Clock.schedule_interval(self.vib_anime,1)
	def on_press(self,*args):
		self.vib_anime()

	def vib_anime(self,*args):
		ctr=self.angle
		an=Animation(angle=(ctr-10)%360,d=.035)+Animation(angle=(ctr+10)%360,d=.035)+Animation(angle=ctr,d=.035)
		
		for i in range(5):
			an+=an
		an.start(self) 

class WinScreen(Screen):
	

	def __init__(self,**kwargs):
		Builder.load_file('wi.kv')
		self.in_action=SoundLoader.load('sound/wi/back.ogg')
		super(WinScreen,self).__init__(**kwargs)
		
		
	
	def back(self,*args):
		self.ani.start(self.ids.backgr)
	def on_enter(self):
		Clock.schedule_interval(self.back,.35)
		self.ani=Animation(opacity=.5,d=.15)+Animation(opacity=1,d=.2)

		self.in_action.play()
		self.an=Animation(opacity=1,d=.1)&Animation(size_hint=(.2,.2),d=.4)+Animation(opacity=0,d=.1)
		self.fires=[Image(opacity=0,source='image/wi/fireworks.png',size_hint=(.1,.1)) for i in range(10)]
		for i in self.fires:self.add_widget(i)
		self.j=0
		Clock.schedule_interval(self.work,.1)

	def work(self,*args):
		i=self.fires[self.j]
		i.size_hint=(.1,.1)
		i.pos_hint={'center_x':(randint(0,8)+.5)/10.0,'center_y':(randint(0,8)+.5)/10.0}
		self.an.start(i)
		self.j=(self.j+1)%10
		

	def on_pre_leave(self):
		self.in_action.stop()

