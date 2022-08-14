
from PIL import Image, ImageDraw, ImageFont, ImageOps
import copy

class Surface:
	def __init__(self, size, color=(0,0,0)):
		self._surf = Image.new('RGBA', size, color)
		self._draw = ImageDraw.Draw(self._surf)

	def blit(self, surface, xy_or_rect):
		if isinstance(xy_or_rect, Rect):
			x = xy_or_rect.x
			y = xy_or_rect.y
		else:
			x = xy_or_rect[0]
			y = xy_or_rect[1]

		surf = surface._surf.convert('RGBA')
		self._surf.paste(surf, (x, y), surf)

	def copy(self):
		return copy.deepcopy(self)

	def fill(self, rgb):
		self._draw.rectangle([(0,0), self._surf.size], fill=rgb)

	def get_rect(self, **kwargs):
		size = self._surf.size
		rect = Rect((0,0),size)

		for place in ('topleft', 'topright', 'top', 'bottomleft', 'bottomright', 'bottom', 'midtop','midleft', 'midright', 'midbottom', 'center', 'centerx', 'centery', 'left', 'right'):
			value = kwargs.pop(place, None)
			if value is not None:
				setattr(rect, place, value)
				return rect

	def get_size(self):
		return self._surf.size

	def get_width(self):
		return self._surf.size[0]

	def get_height(self):
		return self._surf.size[1]


class Rect:
	def __init__(self, left, top, width=None, height=None):
		self.update(left, top, width, height)

	def __repr__(self):
		return f"<rect({self.x}, {self.y}, {self.width}, {self.height})>"




	@property
	def h(self):
		return self.height
	@h.setter
	def h(self, value):
		self.height = value

	@property
	def w(self):
		return self.width
	@w.setter
	def w(self, value):
		self.width = value

	@property
	def right(self):
		return self.x+self.width
	@right.setter
	def right(self, value):
		self.x = value-self.width

	@property
	def left(self):
		return self.x
	@left.setter
	def left(self, value):
		self.x = value




	@property
	def bottom(self):
		return self.y+self.height
	@bottom.setter
	def bottom(self, value):
		self.y = value-self.height

	@property
	def bottomleft(self):
		return (self.x, self.y+self.height)
	@bottomleft.setter
	def bottomleft(self, value):
		self.x = value[0]
		self.bottom = value[1]-self.height

	@property
	def bottomright(self):
		return (self.x+self.width, self.y+self.height)
	@bottomright.setter
	def bottomright(self, value):
		self.right = self.width-value[0]
		self.y = self.height-value[1]




	@property
	def center(self):
		return (self.x+self.width//2, self.y+self.height//2)
	@center.setter
	def center(self, value):
		self.x = value[0]-self.width//2
		self.y = value[1]-self.height//2

	@property
	def centerx(self):
		return self.x-self.width//2
	@centerx.setter
	def centerx(self, value):
		self.x = value-self.width//2

	@property
	def centery(self):
		return self.y-self.height//2
	@centery.setter
	def centery(self, value):
		self.y = value-self.height//2




	@property
	def midbottom(self):
		return (self.centerx, self.bottom)
	@midbottom.setter
	def midbottom(self, value):
		self.bottom = value[0]
		self.centerx = value[1]

	@property
	def midleft(self):
		return (self.x, self.centery)
	@midleft.setter
	def midleft(self, value):
		self.x = value[0]
		self.centery = value[1]

	@property
	def midright(self):
		return (self.right, self.centery)
	@midright.setter
	def midright(self, value):
		self.right = value[0]
		self.centery = value[1]

	@property
	def midtop(self):
		return (self.centerx, self.y)
	@midtop.setter
	def midtop(self, value):
		self.centerx = value[0]
		self.y = value[1]




	@property
	def top(self):
		return self.y
	@top.setter
	def top(self, value):
		self.y = value

	@property
	def topleft(self):
		return (self.x, self.y)
	@topleft.setter
	def topleft(self, value):
		self.x = value[0]
		self.y = value[1]

	@property
	def topright(self):
		return (self.right, self.y)
	@topright.setter
	def topright(self, value):
		self.right = value[0]
		self.y = value[1]


	def move(self, x=0, y=0):
		return Rect((self.x+x, self.y+y), self.size())


	def size(self):
		return (self.width, self.height)


	def copy(self):
		return copy.deepcopy(self)


	def update(self, left, top, width=None, height=None):
		if isinstance(left, tuple):
			self.height = int(top[1])
			self.width  = int(top[0])
			self.x      = int(left[0])
			self.y      = int(left[1])
		else:
			self.height = int(height)
			self.width  = int(width)
			self.x      = int(left)
			self.y      = int(top)

		self.h = self.height
		self.w = self.width


	def collidedict(self, dct):
		...

	def collidedictall(self, dct):
		...

	def collidelist(self, lst):
		for num, rect in enumerate(lst):
			if self.colliderect(rect):
				return num
		return -1

	def collidelistall(self, lst):
		numbers = []
		for num, rect in enumerate(lst):
			if self.colliderect(rect):
				numbers.append(num)
		return numbers

	def collidepoint(self, point):
		return point[0] in range(self.x, self.right()) and point[1] in range(self.y, self.bottom())

	def colliderect(self, rect):
		return rect.x in range(self.x, self.right()) and rect.y in range(self.y, self.bottom())

class draw:

	def rect(surface, color, rect, width=None, *, border_radius=0):
		draw = surface._draw
		if border_radius:
			draw.rounded_rectangle([rect.topleft, rect.bottomright], fill=None if width else color, width=width, outline=color, radius=border_radius)
		else:
			draw.rectangle([rect.topleft, rect.bottomrigh], fill=None if width else color, width=width, outline=color)

	def aaline(surface, color, start_pos, end_pos):
		draw = surface._draw
		draw.line(start_pos + end_pos, fill=color, width=1)

	# def arc(surface, color, rect, start_angle, stop_angle, *, width=1):
	# 	draw = surface._draw
	# 	draw.arc([rect.topleft(), rect.bottomright()], start_angle, stop_angle, fill=color, width=width)

	def circle(surface, color, center, radius, width=0):
		draw = surface._draw
		draw.ellipse([(center[0]-radius, center[1]-radius), (center[0]+radius, center[1]+radius)], fill=None if width else color, outline=color, width=width)

	def ellipse(surface, color, rect, width=0):
		draw = surface._draw
		draw.ellipse([rect.topleft, rect.bottomright], fill=None if width else color, outline=color, width=width)		

	def line(surface, color, start_pos, end_pos, width=1):
		draw = surface._draw
		draw.line(start_pos + end_pos, fill=color, width=width)

	def polygon(surface, color, points, width=0):
		draw = surface._draw
		draw.polygon(points, fill=None if width else color, outline=color, width=width)

class Font:
	def __init__(self, path, size=10):
		self._font = ImageFont.truetype(path, size)

	def render(self, text, antialias, color, *, background=None):
		height = self._font.getbbox(text)[3]*2 - self._font.getbbox(text)[1]
		width = self._font.getbbox(text)[2]*2 - self._font.getbbox(text)[0]
		width //= 2
		text_surf =  Surface((width, height))
		text_surf.fill(background or (0,0,0,0))
		draw = text_surf._draw
		draw.text((0, 0), text, fill=color, font=self._font)
		return text_surf

class image:

	def load(path):
		img = Image.open(path).convert('RGBA')
		img_surf =  Surface(img.size)
		
		surf = img_surf._surf
		surf.paste(img, (0,0))

		return img_surf

	def save(surface, filename):
		surface._surf.save(filename)

	def tostring(surface, mode):
		return surface._surf.convert(mode).tobytes()

class transform:

	def average_color(surface, rect=None): # not correct yet
		im = surface._surf
		r_lst = []
		g_lst = []
		b_lst = []

		len_ = surface.get_size()[0]*surface.get_size()[1]

		for pixel_num, tup in im.getcolors():
			r, g, b, a = tup
			r_lst += [r]*pixel_num
			g_lst += [g]*pixel_num
			b_lst += [b]*pixel_num

		average_r = sum(r_lst) // len_
		average_b = sum(b_lst) // len_
		average_g = sum(g_lst) // len_

		return (average_r, average_g, average_b, 0)

	def chop(surface, rect): # not correct yet
		im = surface._surf

		im_width, im_height = im.size

		size_x, size_y = rect.x-rect.w, rect.y-rect.h

		surf = Surface((im_width+size_x, im_height+size_y))
		surf._surf.paste(im, (size_x, size_y))
		return surf

	def flip(surface, flip_x, flip_y):
		im = surface._surf

		surf = Surface(im.size)

		if flip_x:
			im = ImageOps.mirror(im)
		if flip_y:
			im = ImageOps.flip(im)

		surf._surf.paste(im, (0,0))
		return surf

	def rotate(surface, angle):
		im = surface._surf
		surf = Surface(im.size)

		im = im.rotate(angle, expand=True, fillcolor=(0,0,0,0))
		surf._surf.paste(im, (0,0))
		return surf

	def rotozoom(surface, angle, scale):
		...

	def scale(surface, size):
		im = surface._surf
		surf = Surface(size)

		im = im.resize(size)
		surf._surf.paste(im, (0,0))
		return surf

