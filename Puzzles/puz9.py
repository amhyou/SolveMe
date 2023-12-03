import os
import ssl
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()
from urllib import request

from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.properties import ObjectProperty,ListProperty,NumericProperty,StringProperty
from functools import partial
from kivy.clock import Clock
from random import choice,randint
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang import Builder 


class Bic9(ButtonBehavior,Image):
	angle=NumericProperty(None)
	def __init__(self,**kwargs):
		super(Bic9,self).__init__(**kwargs)
		self.angle=0
	def on_press(self,*args):
		self.vib_anime()

	def vib_anime(self):
		ctr=self.angle
		an=Animation(angle=(ctr-10)%360,d=.035)+Animation(angle=(ctr+10)%360,d=.035)+Animation(angle=ctr,d=.035)
		
		for i in range(5):
			an+=an
		an.start(self) 

class Puz9(Screen):
	sm=ObjectProperty()
	xpath='/html/body/c-wiz/div/div[3]/main/div[2]/c-wiz/div/div[1]/div[1]/div/div[1]/div[1]/div/div[1]/div/span/div/div//text()'
	url='https://www.google.com/finance/quote/ETH-USD'
	win_cl=SoundLoader.load('sound/tr/win.wav')
	lst_cl=SoundLoader.load('sound/tr/lost.wav')
	cash=SoundLoader.load('sound/p9/cash.wav')
	in_action=''
	

	def __init__(self,**kwargs):
		Builder.load_file('Puzzles/puz9.kv')
		self.back=SoundLoader.load('sound/p9/back.ogg')
		super(Puz9,self).__init__(**kwargs)
		

	def on_enter(self):

		self.back.play()

		self.sm=App.get_running_app()
		
	def verify(self):
		try:
			response=request.urlopen(self.url)
			res=response.read().decode('utf-8')

			ds='<div class="YMlKec fxKbKc">'
			i=res.index(ds)+len(ds)
			j=i+res[i:].index('.')
			ans=res[i:j].replace(',','')
			if ans==self.ids.att.text:
				self.ids.att.text='Good!'
				self.ids.att.foreground_color=(.1,1,.1,1)
				self.win_cl.play()
				Clock.schedule_once(partial(self.sm.change,'win_screen'),4)
			else:
				self.ids.att.text='Wrong!'
				self.ids.att.foreground_color=(1,.1,.1,1)
				self.lst_cl.play()
				Clock.schedule_once(partial(self.sm.change,'loose_screen'),4)
				
		except:
			print('your internet conexion is not okay')
			self.ids.err.opacity=1
		
	
	def on_pre_leave(self):
		self.back.stop()

	def on_leave(self):
		self.ids.err.opacity=0
		self.ids.att.text=''
		self.ids.att.foreground_color=(0,0,0,1)