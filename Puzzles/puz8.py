from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty,ListProperty,NumericProperty,StringProperty,BooleanProperty
from functools import partial
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from random import randint,choice,shuffle
from kivy.lang import Builder 
from kivy.app import App
from kivy.uix.label import Label

class Bic8(ButtonBehavior,Label):
	angle=NumericProperty(None)
	yy=NumericProperty()
	xx=NumericProperty()
	viy=NumericProperty()
	vix=NumericProperty()
	sx=NumericProperty()
	sy=NumericProperty()
	num=NumericProperty()
	def __init__(self,num=0,**kwargs):
		super(Bic8,self).__init__(**kwargs)
		self.angle=0
		self.yy=0
		self.xx=0
		self.viy=0
		self.vix=0
		self.sy=1
		self.sx=1
		self.num=num
		self.cap=False
		
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

	def on_touch_down(self,t,*args):
		if self.collide_point(*t.pos):
			self.cap=True
			
	def on_touch_move(self,t,*args):
		if self.cap:
			self.center=t.pos
	def on_touch_up(self,t,*args):
		self.cap=False


class Puz8(Screen):
	app=App.get_running_app()

	def __init__(self,**kwargs):
		Builder.load_file('Puzzles/puz8.kv')
		self.back=SoundLoader.load('sound/p8/back.ogg')
		super(Puz8,self).__init__(**kwargs)
		
		# Sound:
		# Image:
		# Anima:
		# Varia:
		self.words="put all the words in the red container except the word help and tap exactly three times in the green circle"
		self.words=self.words.split(" ")
		
		

	def on_enter(self):
		# Sound:
	
		self.back.play()

		self.posi=[(x,y) for x in range(int(.01*self.width),int(.85*self.width),30) for y in range(int(.05*self.height),int(.85*self.height),30)]
		shuffle(self.posi)
		# Image:
		for i in range(len(self.words)):
			sc=Bic8(num=i+1,text=self.words[i],size_hint=(.15,.15),pos=self.posi.pop(),halign='center')
			sc.font_size=.35*sc.height
			self.ids.biblio.add_widget(sc)
		# Anima:
		self.tap=0
		

	def logic(self,i,*args):
		if i==0:
			for i in range(len(self.words)):
				d=self.ids.biblio.children[i]
				d.text=str(d.num)
		else:
			for i in range(len(self.words)):
				d=self.ids.biblio.children[i]
				d.text=self.words[d.num-1]

	def verify(self,cl=0,*args):
		if not cl:
			self.tap+=1
		if self.tap==1 and not cl:
			for i in self.ids.biblio.children:
				print(i.center)
				if self.words[i.num-1]=='help':
					if self.ids.container.collide_point(*i.center):
						print('loose lwl')
						self.ids.ver.disabled=True
						self.wilo(b=0)
						#self.tap=0
						break
				elif not self.ids.container.collide_point(*i.center):
					print('loose lwl')
					self.ids.ver.disabled=True
					self.wilo(b=0)
					#self.tap=0
					break
					
			else:
				Clock.schedule_once(partial(self.verify,1),1)
			

		elif cl:
			#self.ids.ver.disabled=True
			if self.tap==3:
				print('win')
				self.wilo()
			else:
				print('loose tani')
				self.wilo(b=0)
			self.tap=0
		

		

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