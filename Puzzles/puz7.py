from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty,ListProperty,NumericProperty,StringProperty,BooleanProperty
from functools import partial
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from random import randint,choice
from kivy.lang import Builder 
from kivy.app import App
class Bic7(ButtonBehavior,Image):
	angle=NumericProperty(None)
	yy=NumericProperty()
	xx=NumericProperty()
	viy=NumericProperty()
	vix=NumericProperty()
	sx=NumericProperty()
	sy=NumericProperty()
	num=NumericProperty()
	def __init__(self,num,**kwargs):
		super(Bic7,self).__init__(**kwargs)
		self.angle=0
		self.yy=0
		self.xx=0
		self.viy=0
		self.vix=0
		self.sy=1
		self.sx=1
		self.num=num
		self.clicked=False
		
	def vib_anime(self):
		ctr=self.angle
		an=Animation(angle=(ctr-30)%360,d=.1)+Animation(angle=(ctr+30)%360,d=.1)+Animation(angle=ctr,d=.1)
		an.start(self) 
	def scl_anime(self,*args):
		an=Animation(sx=1.2,sy=1.2,d=.2)+Animation(sx=1/1.2,sy=1/1.2,d=.2)
		an.start(self)
	def translate(self,x,y,*args):
		an=Animation(center=(x,y),d=.9)&Animation(opacity=1,d=.1)
		an.start(self)

	def vib(self,dx,dy,*args):
		x,y=self.xx+dx,self.yy+dy
		if x>=1280/2:x=1280/2
		elif x<=0:x=0
		if y>=720/3.0:y=720/3.0
		elif y<=-720/3.0:y=-720/3.0
		an=Animation(xx=x,yy=y,d=.1)
		an.start(self) 
	def on_release(self,*args):
		if not self.clicked:
			Puz7.app.sm.get_screen('puz7').verify(self.num,self)
			self.clicked=True

			

class Puz7(Screen):
	app=App.get_running_app()
	elm={1:'computer',2:'flower',3:'heart',4:'candy',5:'x'}
	def __init__(self,**kwargs):
		Builder.load_file('Puzzles/puz7.kv')
		self.back=SoundLoader.load('sound/p7/back.ogg')
		super(Puz7,self).__init__(**kwargs)
		
		# Sound:
		# Image:
		# Anima:
		# Varia:


	def on_enter(self):
		# Sound:

		self.back.play()
		self.cnt=[0,0,0,0]
		self.options=[1,2,3,4,5]
		self.ids.biblio.clear_widgets()
		
		# Image:
		for i in range(9):
			j=choice(self.options)
			if j==5:
				self.options.pop(self.options.index(5))
			else:
				self.cnt[j-1]+=1
				if self.cnt[j-1]==2:
					self.options.pop(self.options.index(j))
			self.ids.biblio.add_widget(Bic7(num=j,source='image/p7/question.png'))
		# Anima:
		
		self.match=False
		self.nm=None
		
		self.stage=0
		self.t=True	
		Clock.schedule_once(self.logic,.8)

	def logic(self,*args):
		if self.t:
			for i in range(9):
				j=self.ids.biblio.children[i]
				j.source='image/p7/'+self.elm[j.num]+'.png'
			self.t=False
			Clock.schedule_once(self.logic,1.2)
		else:
			for i in range(9):
				j=self.ids.biblio.children[i]
				j.source='image/p7/question.png'
			self.t=True



	def verify(self,num,obj,*args):
		obj.source='image/p7/'+self.elm[num]+'.png'
		if not self.match:
			self.match=True
			self.nm=num
		else:
			if self.nm==num:
				self.stage+=1
				if self.stage==4:
					self.wilo()
				
			else:
				self.wilo(b=0)
			self.match=False
			self.nm=None

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