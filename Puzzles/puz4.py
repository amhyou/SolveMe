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
class Bic4(ButtonBehavior,Image):
	angle=NumericProperty(None)
	yy=NumericProperty()
	xx=NumericProperty()
	viy=NumericProperty()
	vix=NumericProperty()
	sx=NumericProperty()
	sy=NumericProperty()
	num=NumericProperty()
	def __init__(self,**kwargs):
		super(Bic4,self).__init__(**kwargs)
		self.angle=0
		self.yy=0
		self.xx=0
		self.viy=0
		self.vix=0
		self.sy=1
		self.sx=1
		
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

			
from joystick import Joystick


class Puz4(Screen):
	app=App.get_running_app()
	ver=True
	jx=NumericProperty(0)
	jy=NumericProperty(0)
	def __init__(self,**kwargs):
		Builder.load_file('Puzzles/puz4.kv')
		self.back=SoundLoader.load('sound/p4/back.ogg')
		super(Puz4,self).__init__(**kwargs)
		
		# Sound:
		
		# Image:
		self.joystick = Joystick(size_hint=(.2,.2),pos_hint={'cente_x': .1,"center_y":.2})
		self.joystick.bind(pad=self.update_coordinates)
		
		# Anima:
		# Varia:
		self.im=0
		self.pr=True


	def on_enter(self):
		# Sound:
		
		self.ids.aze.center=(0,720/2)

		self.back.play()
		# Image:
		self.add_widget(self.joystick)
		# Anima:
		
		self.lo=Clock.schedule_interval(self.logic,.2)
		self.fi=Clock.schedule_interval(self.fire,randint(7,10)/7)
		self.vr=Clock.schedule_interval(self.verify,1/60.0)
		self.i=0
	def fire(self,*args):
		aze=self.ids['fire'+str(self.i+1)]
		aze.yy=0
		aze.opacity=1
		aze.translate()
		self.i=(self.i+1)%3
	def logic(self,*args):
		if self.jx!=0 or self.jy!=0:
			self.ids.aze.vib(self.jx,self.jy)
			self.im=(self.im+1)%8
			if self.jx>=0:
				self.pr=True
				self.ids.aze.source='image/p4/'+str(self.im+1)+'.png'
			else:
				self.pr=False
				self.ids.aze.source='image/p4/'+str(self.im+1)*2+'.png'

		else:
			if self.pr:
				self.ids.aze.source='image/p4/1.png'
			else:
				self.ids.aze.source='image/p4/11.png'
			self.im=0

	def update_coordinates(self, joystick, pad):
		self.jx = pad[0]*50
		self.jy = pad[1]*50
		
	def verify(self,*args):
		bb=self.ids.aze
		if self.ids.door.collide_point(bb.center[0]+bb.xx,bb.center[1]+bb.yy):
			self.wilo()
			self.lo.cancel()
			self.fi.cancel()
			self.vr.cancel()
		else:
			for i in range(3):
				cc=self.ids['fire'+str(i+1)]
				cx=(.2+.3*i)*self.width
				cy=cc.center[1]+cc.yy
				bx,by=bb.center[0]+bb.xx,bb.center[1]+bb.yy
				if abs(cx-bx)<.05*self.width and abs(cy-by)<.03*self.height:
					self.wilo(b=0)
					self.lo.cancel()
					self.fi.cancel()
					self.vr.cancel()
					break
			

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
		self.remove_widget(self.joystick)
		# Anime:
		
		# Varia:
		bb=self.ids.aze
		bb.vib(-bb.xx,-bb.yy)
