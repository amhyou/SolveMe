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
class Bic6(ButtonBehavior,Image):
	angle=NumericProperty(None)
	yy=NumericProperty()
	xx=NumericProperty()
	viy=NumericProperty()
	vix=NumericProperty()
	sx=NumericProperty()
	sy=NumericProperty()
	num=NumericProperty()
	def __init__(self,**kwargs):
		super(Bic6,self).__init__(**kwargs)
		self.angle=0
		self.yy=0
		self.xx=0
		self.viy=0
		self.vix=0
		self.sy=1
		self.sx=1
		
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

			
from joystick import Joystick


class Puz6(Screen):
	app=App.get_running_app()
	ver=True
	jx=NumericProperty(0)
	jy=NumericProperty(0)
	death=NumericProperty(0)
	def __init__(self,**kwargs):
		Builder.load_file('Puzzles/puz6.kv')
		self.back=SoundLoader.load('sound/p6/back.ogg')
		super(Puz6,self).__init__(**kwargs)
		
		# Sound:
		
		# Image:
		self.joystick = Joystick(size_hint=(.2,.2),pos_hint={'cente_x':.1,"center_y":.2})
		self.joystick.bind(pad=self.update_coordinates)
		
		# Anima:
		# Varia:
		self.im=0
		self.pr=True


	def on_enter(self):
		# Sound:

		self.back.play()
		# Image:
		self.add_widget(self.joystick)
		self.ids.gun.opacity=1
		# Anima:
		self.ids.aze.y=720/2
		self.lo=Clock.schedule_interval(self.logic,.1)
		self.fi=Clock.schedule_interval(self.fire,.4)
		self.fi1=Clock.schedule_once(self.fire1,1)
		self.lst=0
		self.bul=0
		self.lastp=0
		self.passed=True
	def fire(self,*args):
		self.ids.gun.vib_anime()
		
	def fire1(self,*args):
		x,y=self.ids.aze.center[0]+self.ids.aze.xx,self.ids.aze.center[1]+self.ids.aze.yy
		self.ids.bullet.opacity=0
		self.ids.bullet.center=(.87*self.width,.337*self.height)
		a,b=self.ids.bullet.center
		self.ids.bullet.translate(0,b-a*(y-b)/(x-a))
		self.bul+=1
		if self.bul<7:
			self.fi1=Clock.schedule_once(self.fire1,1)
		elif self.passed:
			self.ids.gun.opacity=0
			self.ids.bullet.opacity=0
			self.wilo()

	def logic(self,*args):
		self.verify()
		if self.jx!=0 or self.jy!=0:
			self.ids.aze.vib(self.jx,self.jy)
			self.im=(self.im+1)%17
			if self.jx>=0:
				self.pr=True
				self.ids.aze.source='image/p6/0'+str(self.im+1)+'.png'
			else:
				self.pr=False
				self.ids.aze.source='image/p6/'+str(self.im+1)+'.png'

		else:
			if self.pr:
				self.ids.aze.source='image/p6/01.png'
			else:
				self.ids.aze.source='image/p6/1.png'
			self.im=0

	def update_coordinates(self, joystick, pad):
		self.jx = pad[0]*50
		self.jy = pad[1]*50
		
	def verify(self,*args):
		if self.ids.aze.collide_widget(self.ids.bullet) and self.lastp!=self.bul:
			self.lst+=1
			self.death+=1
			print('lost',self.lst)
			self.lastp=self.bul
			if self.lst==3:
				self.ids.gun.opacity=0
				self.fi1.cancel()
				self.passed=False
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
		self.lo.cancel()
		self.fi.cancel()
		self.fi1.cancel()
		# Varia:
		self.remove_widget(self.joystick)
		self.death=0
