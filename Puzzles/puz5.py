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
class Bic5(ButtonBehavior,Image):
	angle=NumericProperty(None)
	yy=NumericProperty()
	xx=NumericProperty()
	viy=NumericProperty()
	vix=NumericProperty()
	sx=NumericProperty()
	sy=NumericProperty()
	num=NumericProperty()
	def __init__(self,**kwargs):
		super(Bic5,self).__init__(**kwargs)
		self.angle=0
		self.yy=0
		self.xx=0
		self.viy=0
		self.vix=0
		self.sy=1
		self.sx=1
		self.cap=False
		
	def vib_anime(self):
		ctr=self.angle
		an=Animation(angle=(ctr-10)%360,d=.035)+Animation(angle=(ctr+10)%360,d=.035)+Animation(angle=ctr,d=.035)
		an.start(self) 
	def scl_anime(self,*args):
		an=Animation(sx=1.2,sy=1.2,d=.2)+Animation(sx=1/1.2,sy=1/1.2,d=.2)
		an.start(self)
	def translate(self,*args):
		an=Animation(yy=720,d=.25)+Animation(opacity=0,d=.01)
		an.start(self)

	def vib(self,dx,dy,*args):
		x,y=self.xx+dx,self.yy+dy
		if x>=1280:x=1280
		elif x<=0:x=0
		if y>=720/3.0:y=720/3.0
		elif y<=-720/3.0:y=-720/3.0
		an=Animation(xx=x,yy=y,d=.1)
		an.start(self) 
	def on_touch_down(self,t,*args):
		if self.collide_point(*t.pos):
			self.cap=True
	def on_touch_move(self,t,*args):
		if self.cap:
			self.center=t.pos
			Puz5.app.sm.get_screen('puz5').logic(*t.pos)
	def on_touch_up(self,t,*args):
		if self.cap:
			Puz5.app.sm.get_screen('puz5').verify(*t.pos)
		self.cap=False

			

from kivy.graphics.vertex_instructions import Rectangle
class Puz5(Screen):
	app=App.get_running_app()
	def __init__(self,**kwargs):
		Builder.load_file('Puzzles/puz5.kv')
		self.back=SoundLoader.load('sound/p5/back.ogg')
		super(Puz5,self).__init__(**kwargs)
		
		# Sound:
		
		# Image:
		self.im=Image(source='image/p5/indicator.png',size_hint=(.2,.1),pos_hint={'center_x':.5,'center_y':.5}).texture
		self.imy=Image(source='image/p5/indicatory.png',size_hint=(.1,.2),pos_hint={'center_x':.5,'center_y':.5}).texture
		#im1=im.get_region(0,0,2315,1876)

		# Anima:
		# Varia:
	
		
	def on_enter(self):
		# Sound:


		self.back.play()
		# Image:
		# Anima:
		#Clock.schedule_interval(self.logic,1)
		# Varia:
		self.answer=(randint(0,self.width),randint(0,self.height))

	def logic(self,dx,dy,*args):
		x=2315-abs(self.answer[0]-dx)*2315/max(self.answer[0],1876-self.answer[0])
		y=2315-abs(self.answer[1]-dy)*2315/max(self.answer[1],1876-self.answer[1])
		self.im1=self.im.get_region(0,0,x,400)
		self.im2=self.imy.get_region(1876-300,0,400,y)
		with self.canvas.after:
			self.canvas.after.clear()
			Rectangle(texture=self.im1,pos=(.05*self.width,.15*self.height),size=(.2*self.width*x/2315,.08*self.height))
			Rectangle(texture=self.im2,pos=(.03*self.width,.3*self.height),size=(.08*self.width,.2*self.height*y/2315))
	def verify(self,x,y,*args):
		if abs(x-self.answer[0])<.1*self.width and abs(self.answer[1]-y)<.05*self.width:
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