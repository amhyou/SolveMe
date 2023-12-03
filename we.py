from kivy.uix.screenmanager import Screen

from kivy.properties import ObjectProperty,ListProperty,NumericProperty,StringProperty

from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from functools import partial
from collections import deque
from random import randint

class Bic(ButtonBehavior,Image):
	angle=NumericProperty(None)
	sx=NumericProperty()
	sy=NumericProperty()
	def __init__(self,**kwargs):
		super(Bic,self).__init__(**kwargs)
		self.angle=0
		self.sx=1
		self.sy=1
	def on_press(self,*args):
		self.vib_anime()

	def vib_anime(self):
		ctr=self.angle
		an=Animation(angle=(ctr-10)%360,d=.035)+Animation(angle=(ctr+10)%360,d=.035)+Animation(angle=ctr,d=.035)
		
		for i in range(5):
			an+=an
		an.start(self) 
	def vib(self,*args):
		an=Animation(sx=1.2,sy=1.1,d=.2)+Animation(sx=1/1.2,sy=1/1.1,d=.2)
		an.start(self)

class WelcomeScreen(Screen):
	app=App.get_running_app()
	back_texture=ObjectProperty(None)
	apple=deque([])
	star=deque([])
	glas=deque([])
	def __init__(self,**kwargs):
		Builder.load_file('we.kv')
		self.back=''
		super(WelcomeScreen,self).__init__(**kwargs)
		# background texture
		self.back_texture = Image(source="image/we/sky.png").texture
		self.back_texture.wrap = 'repeat'
		self.back_texture.uvsize = (self.width / self.back_texture.width, -1)
	

	def on_size(self, *args):
		self.back_texture.uvsize = (self.width / (2*self.back_texture.width), -1)
		
	def scroll_textures(self, time_passed):
		# Update the uvpos of the texture
		self.back_texture.uvpos = ( (self.back_texture.uvpos[0] + time_passed/4.0)%self.width , self.back_texture.uvpos[1])

		# Redraw the texture
		texture = self.property('back_texture')
		texture.dispatch(self)

	def on_enter(self):
	
		if self.back!='':
			self.back.play()
		Clock.schedule_once(self.button,1.5)
		Clock.schedule_interval(self.scroll_textures, 7/60.)
		self.bee=Image(source='image/we/bee.png',size_hint=(.3,.3))
		self.bee.pos_hint={'center_x':randint(2,8)/10.0,'center_y':randint(2,8)/10.0}
		self.create_bee()
		Clock.schedule_interval(self.anime_welc,.4)
	def button(self,*args):
		an=Animation(size_hint=(.23,.3),d=.7)
		an.start(self.ids.start)
	def anime_welc(self,*args):
		
		az1=self.ids.welcome
		az1.vib()
		az2=self.ids.tothe
		az2.vib()
		az3=self.ids.game
		az3.vib()
	def	on_touch_down(self,*args):
		if self.ids.start.collide_point(*args[0].pos):
			self.start()
		elif self.bee.collide_point(*args[0].pos):
			self.apple.append(Image(source='image/we/apple.png',size_hint=(.05,.05),pos_hint={'center_x':args[0].pos[0]/self.width,'center_y':args[0].pos[1]/self.height}))
			self.add_widget(self.apple[-1])
			an3=Animation(pos_hint={'center_x':args[0].pos[0]/self.width,'center_y':(args[0].pos[1]+100)/self.height},size_hint=(.1,.1),d=.5)+Animation(pos_hint={'center_x':args[0].pos[0]/self.width,'center_y':(args[0].pos[1]+40)/self.height},d=.3)
			an3.start(self.apple[-1])
	
			Clock.schedule_once(partial(self.glass,args[0].pos),.9)
		else:
			self.star.append(Image(source='image/we/star.png',opacity=0,size_hint=(.1,.1),pos_hint={'center_x':args[0].pos[0]/self.width,'center_y':args[0].pos[1]/self.height}))
			self.add_widget(self.star[-1])
			an1=Animation(opacity=1,pos_hint={'center_x':args[0].pos[0]/self.width,'center_y':(args[0].pos[1]+100)/self.height})+Animation(opacity=0)
			an1.start(self.star[-1])
			an2=Animation(opacity=.5,d=.1)+Animation(opacity=1,d=.1)
			an2.start(self.ids.start)
			Clock.schedule_once(self.remove,2)
	def glass(self,pos,*args):
		self.glas.append(Image(source='image/we/oh.png',size_hint=(.3,.3),pos_hint={'center_x':pos[0]/self.width,'center_y':(pos[1]+40)/self.height}))
		self.add_widget(self.glas[-1])
		self.remove_widget(self.apple[0])
		self.apple.popleft()
	def remove(self,*args):
		self.remove_widget(self.star[0])
		self.star.popleft()
		
	def start(self):
		an=Animation(size_hint=(50,50),d=2)
		an.start(self.ids.start)
		Clock.schedule_once(partial(self.app.change,'puz8'),1)
		Clock.schedule_once(self.get_rid,2)

	def create_bee(self,*args):
		self.add_widget(self.bee)
		self.rbee=Clock.schedule_once(self.remove_bee,.8)
		
	def remove_bee(self,*args):
		self.remove_widget(self.bee)
		self.bee.pos_hint={'center_x':(randint(0,8)+.5)/10.0,'center_y':(randint(0,8)+.5)/10.0}
		self.cbee=Clock.schedule_once(self.create_bee,.7)

	def get_rid(self,*args):
		self.remove_widget(self.bee)
		for i in self.glas:
			self.remove_widget(i)
		self.glas=deque([])
		self.rbee.cancel()
		self.cbee.cancel()

	def on_leave(self):
		if self.back!='':
			self.back.stop()
		