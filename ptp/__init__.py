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
		topleft     = kwargs.pop('topleft', None)
		topright    = kwargs.pop('topright', None)
		top         = kwargs.pop('top', None)

		bottomleft  = kwargs.pop('bottomleft', None)
		bottomright = kwargs.pop('bottomright', None)
		bottom      = kwargs.pop('bottom', None)

		midtop      = kwargs.pop('midtop', None)
		midleft     = kwargs.pop('midleft', None)
		midright    = kwargs.pop('midright', None)
		midbottom   = kwargs.pop('midbottom', None)

		center      = kwargs.pop('center', None)
		centerx     = kwargs.pop('centerx', None)
		centery     = kwargs.pop('centery', None)

		left        = kwargs.pop('left', None)
		right       = kwargs.pop('right', None)

		if all(i is None for i in [topleft, topright, top, bottomleft, bottomright, bottom, midtop, midleft, midright, midbottom, center, centerx, centery, left, right]):
			return

		size = self._surf.size
		if topleft is not None:
			return Rect(topleft, size)
		if topright is not None:
			return Rect((topright[0]-size[0], topright[1]), size)
		if top is not None:
			return Rect((0, top), size)

		if bottomleft is not None:
			return Rect((bottomleft[0], bottomleft[1]-size[1]), size)
		if bottomright is not None:
			return Rect((bottomright[0]-size[0], bottomright[1]-size[1]), size)
		if bottom is not None:
			return Rect((0, bottom-size[1]), size)

		if midtop is not None:
			return Rect((midtop[0]-size[0]//2, midtop[1]), size)
		if midleft is not None:
			return Rect((midleft[0], midleft[1]-size[1]//2), size)
		if midright is not None:
			return Rect((midright[0]-size[0], midright[1]-size[1]//2), size)
		if midbottom is not None:
			return Rect((midbottom[0]-size[0]//2, midbottom[1]-size[1]), size)

		if center is not None:
			return Rect((center[0]-size[0]//2, center[1]-size[1]//2), size)
		if centerx is not None:
			return Rect((centerx-size[0]//2, 0), size)
		if centery is not None:
			return Rect((0, centery-size[1]//2), size)

		if left is not None:
			return Rect((left, 0), size)
		if right is not None:
			return Rect((right-size[0], 0), size)

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

	def bottom(self):
		return self.y+self.height

	def bottomleft(self):
		return (self.x, self.y+self.height)

	def bottomright(self):
		return (self.x+self.width, self.y+self.height)


	def center(self):
		return (self.x+self.width//2, self.y+self.height//2)

	def centerx(self):
		return self.x+self.width//2

	def centery(self):
		return self.y+self.height//2


	def midbottom(self):
		return (self.centerx(), self.y+self.height)

	def midleft(self):
		return (self.x, self.centery())

	def midright(self):
		return (self.x+self.width, self.centery())	
	
	def midtop(self):
		return(self.centerx(), self.y)


	def topleft(self):
		return (self.x, self.y)

	def topright(self):
		return (self.x+self.width, self.y)


	def right(self):
		return self.x+self.width



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
			self.left   = int(left[0])
			self.top    = int(left[1])
		else:
			self.height = int(height)
			self.width  = int(width)
			self.left   = int(left)
			self.top    = int(top)

		self.x = self.left
		self.y = self.top

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
			draw.rounded_rectangle([rect.topleft(), rect.bottomright()], fill=None if width else color, width=width, outline=color, radius=border_radius)
		else:
			draw.rectangle([rect.topleft(), rect.bottomright()], fill=None if width else color, width=width, outline=color)

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
		draw.ellipse([rect.topleft(), rect.bottomright()], fill=None if width else color, outline=color, width=width)		

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