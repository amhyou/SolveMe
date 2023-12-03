from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty,ListProperty,NumericProperty,StringProperty
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
def vibrate(pos,size,er=0.05,err=0.1):
	tp,cx=pos['top'],pos['center_x']
	w,h=size
	op=Animation(opacity=0,d=.7)+Animation(opacity=1,d=0.7)
	sc0=Animation(size_hint=(w*(1+err),h*(1+err)),d=.15)+Animation(size_hint=(w*(1-err), h*(1-err)), d=.15)+Animation(size_hint=(w, h), d=.15)
	sc1=Animation(size_hint=(w*(1+err),h*(1+err)),d=.15)+Animation(size_hint=(w*(1-err), h*(1-err)), d=.15)+Animation(size_hint=(w, h), d=.15)
	sc2=Animation(size_hint=(w*(1+err),h*(1+err)),d=.15)+Animation(size_hint=(w*(1-err), h*(1-err)), d=.15)+Animation(size_hint=(w, h), d=.15)
	tr0=Animation(pos_hint={"top":tp*(1+er), "center_x":cx*(1+er)},d=.15)+Animation(pos_hint={"top":tp*(1-er), "center_x":cx*(1-er)},d=.15)+Animation(pos_hint={"top":tp, "center_x":cx},d=.15)
	tr1=Animation(pos_hint={"top":tp*(1+er), "center_x":cx*(1+er)},d=.15)+Animation(pos_hint={"top":tp*(1-er), "center_x":cx*(1-er)},d=.15)+Animation(pos_hint={"top":tp, "center_x":cx},d=.15)
	tr2=Animation(pos_hint={"top":tp*(1+er), "center_x":cx*(1+er)},d=.15)+Animation(pos_hint={"top":tp*(1-er), "center_x":cx*(1-er)},d=.15)+Animation(pos_hint={"top":tp, "center_x":cx},d=.15)
	return((tr0+tr1+tr2)&(sc0+sc1+sc2)&op)
from kivy.clock import Clock
from kivy.lang import Builder 


class Bicloose(ButtonBehavior,Image):
	angle=NumericProperty(None)
	sc=NumericProperty(None)
	def __init__(self,**kwargs):
		super(Bicloose,self).__init__(**kwargs)
		self.angle=0
		self.sc=1
		self.an=Clock.schedule_interval(self.vib_anime,2)
	def on_press(self,*args):
		self.vib_anime()

	def vib_anime(self,*args):
		ctr=self.angle
		an=Animation(angle=(ctr-10)%360,d=.035)+Animation(angle=(ctr+10)%360,d=.035)+Animation(angle=ctr,d=.035)
		for i in range(5):
			an+=an
		an.start(self) 
	def vib(self,*args):
		an=Animation(sc=1.2,d=.2)+Animation(sc=1/1.2,d=.2)
		an.start(self)

class LooseScreen(Screen):
	last_session='puz1'
	life_score=NumericProperty(3)
	im=[]
	back_texture=ObjectProperty(None)
	app=App.get_running_app()
	def rotate_face(self):
		face=self.ids['face']
		an=vibrate(face.pos_hint,face.size_hint)
		an.start(face)

	def rotate_frog(self):
		face=self.ids['frog']
		an=vibrate(face.pos_hint,face.size_hint)
		an.start(face)
	def __init__(self,**kwargs):
		Builder.load_file('lo.kv')
		self.in_action=SoundLoader.load('sound/lo/back.ogg')
		#self.baby=SoundLoader.load('sound/lo/baby.ogg')
		#self.heart=SoundLoader.load('sound/lo/heart.ogg')
		#self.frog=SoundLoader.load('sound/lo/frog.ogg')
		super(LooseScreen,self).__init__(**kwargs)
		
		
		# background texture
		self.back_texture = Image(source="image/lo/space.jpg").texture
		self.back_texture.wrap = 'repeat'
		self.back_texture.uvsize = (self.width / self.back_texture.width, -1)
		self.loaded=False

	def on_size(self, *args):
		self.back_texture.uvsize = (self.width / (2*self.back_texture.width), -1)
	
	def scroll_textures(self, time_passed):
		# Update the uvpos of the texture
		self.back_texture.uvpos = ( (self.back_texture.uvpos[0]+ time_passed/4.0)%self.width , (self.back_texture.uvpos[1]+ time_passed/4.0)%self.width)

		# Redraw the texture
		texture = self.property('back_texture')
		texture.dispatch(self)
		
	def on_enter(self):
		Clock.schedule_interval(self.scroll_textures, 10/60.)
		'''
		self.sm=App.get_running_app()
		if self.sm.rew and self.life_score==0:
			self.ids.rew.disabled=False
			self.ids.rew.opacity=1
			self.ids.rew.an=Clock.schedule_interval(self.ids.rew.vib_anime,2)
		else:
			self.ids.rew.disabled=True
			self.ids.rew.opacity=.05
			self.ids.rew.an.cancel()
		'''
		if self.life_score==0:
			self.ids['cont'].disabled=True
			self.ani=Clock.schedule_interval(self.back,.7)
			self.ids['cont'].opacity=.1
			
		else:
			self.ids['back'].opacity=.3
			self.ids['cont'].disabled=False
			self.conti=Clock.schedule_interval(self.ids['cont'].vib,.4)
			

		im1=Image(source='image/lo/health_heart.png',size_hint=(.2,.2),pos_hint={'top':.8,'center_x':.65})
		im2=Image(source='image/lo/health_heart.png',size_hint=(.2,.2),pos_hint={'top':.8,'center_x':.5})
		im3=Image(source='image/lo/health_heart.png',size_hint=(.2,.2),pos_hint={'top':.8,'center_x':.35})
		self.im=[im1,im2,im3]
		for i in range(2,1-self.life_score,-1):
			self.add_widget(self.im[i])
		an=Animation(opacity=0)
		an.start(self.im[i])
		#self.heart.play()
		self.in_action.play()
	def on_pre_leave(self):
		self.in_action.stop()
		#self.baby.stop()

	def on_leave(self):
		if self.life_score==1:
			self.app.root.ids['welcome_screen'].back=SoundLoader.load('sound/we/back.ogg')
		try:
			self.ani.cancel()
			self.conti.cancel()
		except:
			s=1
		self.ids['cont'].opacity=1
		self.ids['back'].opacity=1
		for w in self.im:
			self.remove_widget(w)
	def back(self,*args):
		an=Animation(pos_hint={'x':-.01,'y':0.1},d=.1)+Animation(pos_hint={'x':.01,'y':0.1},d=.1)+Animation(pos_hint={'x':0,'y':0.1},d=.1)
		an.start(self.ids.back)
