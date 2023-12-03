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

class Bic3(ButtonBehavior,Image):
	angle=NumericProperty(0)
	xx=NumericProperty(0)
	yy=NumericProperty(0)
	sx=NumericProperty(1)
	sy=NumericProperty(1)
	num=NumericProperty()
	def __init__(self,**kwargs):

		super(Bic3,self).__init__(**kwargs)
		self.capture=False
		
		
	def on_press(self,*args):
		self.vib_anime()
		self.scl_anime()
	def vib_anime(self):
		ctr=self.angle
		an=Animation(angle=(ctr-10)%360,d=.035)+Animation(angle=(ctr+10)%360,d=.035)+Animation(angle=ctr,d=.035)
		for i in range(5):
			an+=an
		an.start(self) 
	def scl_anime(self,*args):
		an=Animation(sx=1.2,sy=1.2,d=.2)+Animation(sx=1/1.2,sy=1/1.2,d=.2)
		an.start(self)

	def on_release(self,*args):
		self.disabled=True
		Clock.schedule_once(partial(Puz3.app.sm.get_screen('puz3').logic,self.num),1)


class Puz3(Screen):
	app=App.get_running_app()
	nm={1:'chess',2:'tennis',3:'ping'}
	def __init__(self,**kwargs):
		Builder.load_file('Puzzles/puz3.kv')
		self.back=SoundLoader.load('sound/p3/back.ogg')
		super(Puz3,self).__init__(**kwargs)
		
		self.app=App.get_running_app()
		# Sound:
		self.op=[]
		for i in range(1,4):
			c=Bic3(source='image/p3/'+self.nm[i]+'.png')
			c.num=i
			self.op.append(c)
			self.ids.options.add_widget(self.op[-1])
		# Image:
		# Anima:
		# Varia:
		self.i=1
		self.answer=''
		

	def on_enter(self):
		# Sound:
		self.back.play()
		# Image:
		
		self.ids.redoo.disabled=False
			
		# Anima:
	def logic(self,num,*args):
		if self.i<=3 and self.i>=1: 
			self.ids.options.remove_widget(self.op[num-1])
			self.ids['q'+str(self.i)].source='image/p3/'+self.nm[num]+'.png'
			self.answer+=str(num)
		self.i+=1
		if self.i==4:
			self.ids.redoo.disabled=True
			self.verify()

	def redo(self):
		self.i=1
		self.ids.options.clear_widgets()
		for i in range(1,4):
			self.op[i-1].disabled=False
			self.ids.options.add_widget(self.op[i-1])
			self.ids['q'+str(i)].source='image/p3/question.png'

	def verify(self,*args):
		if self.answer=='123':
			self.wilo()
		else:
			self.wilo(b=0)

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
		self.answer=''
		self.redo()
		