from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty,ListProperty,NumericProperty,StringProperty
from kivy.uix.image import Image
from kivy.animation import Animation
from random import randint
from kivy.lang import Builder
from kivy.core.audio import SoundLoader


class Progress(Widget):
	texture = ObjectProperty()
	#head = ObjectProperty(None)
	op=NumericProperty(0)
	stage=NumericProperty(1)
	tex_coords = ListProperty([0, 0, 1, 0, 1, 1, 0, 1])

	

	def __init__(self, **kwargs):
		super(Progress, self).__init__(**kwargs)
		Builder.load_file('tr.kv')
		self.texture=Image(source="image/tr/slide.png").texture
		self.texture.wrap='repeat'
		self.snd=[SoundLoader.load('sound/tr/2.ogg'),SoundLoader.load('sound/tr/1.ogg')]
		self.cgr=SoundLoader.load('sound/tr/cgr.ogg')
		self.hnt=SoundLoader.load('sound/tr/hnt.ogg')

	def score(self,nb):
		self.snd[randint(0,1)].play()
		an=Animation(stage=nb)&Animation(tex_coords=[0,0,15*nb,0,15*nb,1,0,1])
		an.start(self)
