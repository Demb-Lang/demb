import discord
from ReflectionHelper import *
from enum import Enum
from copy import deepcopy

class dembParseException(Exception):pass

class Attribute(Enum):
	Undefined = 0
	Field = 1
	Author = 2

class Embed:
	def __init__(self, name):
		self.Name = name
		self.Fields = []
		self.Author = None
	def set_title(self, title):
		self.title = title
	def set_url(self, url):
		self.url = url
	def set_description(self, desc):
		self.description = desc
	def set_color(self, color):
		try:color = int(color, 16)
		except ValueError: raise dembParseException(f"Invalid color in base 16: {color}")
		self.color = color
	def set_footer(self, f):
		self.footer = f
	def set_thumbnail(self, t):
		self.thumbnail = t
	def set_comment(self, c):
		return
	def Finalize(self):
		rootArgs = ["title", "url", "description", "color"]
		root = {}
		for arg in rootArgs:
			try:root[arg] = GetField(self, arg).GetValue(self)
			except:continue
		emb = discord.Embed(**root)
		try:emb.set_footer(GetField(self, "footer").GetValue(self))
		except:pass
		try:emb.set_thumbnail(url=GetField(self, "thumbnail").GetValue(self))
		except:pass
		for field in self.Fields:emb.add_field(name=field.name, value=field.value, inline=field.inline)
		authorArgs = ["name", "url", "icon_url"]
		if self.Author!=None:
			author = {}
			for arg in authorArgs:
				try:author[arg] = GetField(self.Author, arg).GetValue(self.Author)
				except:continue
			emb.set_author(**author)
		return emb
		
class Field:
	def __init__(self):
		self.name = ""
		self.value = ""
		self.inline = False
	def set_name(self, n):
		self.name = n
	def set_value(self, v):
		self.value = v
	def set_comment(self, c):
		return
	def set_inline(self, i):
		if type(i)!=bool:
			if i == "True" or i=="true":i = True
			elif i == "False" or i=="false":i = False
			else: raise dembParseException(f'Invalid inline value: {i}')
		self.inline = i

class Author:
	def set_name(self, n):
		self.name = n
	def set_link(self, l):
		self.link = l
	def set_icon_url(self, i):
		self.icon_url = i
	def set_comment(self, c):
		return

class Parser:
	def __init__(self, path, **kwargs):
		forceCreate = True
		self.Default = None
		self.parsed = {}
		self.Path = path
		self.defArgs = kwargs
		def delStr(s: str, i = 0) -> str:
			l = list(s)
			del l[i]
			return ''.join(l)
		currentEmb = self.Default
		currentAttr = Attribute.Undefined
		currentAttrName = None
		currentInner = None
		attrDict = {
			Attribute.Undefined: ["title", "comment", "description", "url", "field", "author", "color", "thumbnail", "footer"],
			Attribute.Field: ["name", "comment", "value", "inline", "end"],
			Attribute.Author: ["name", "comment" "url", "icon_url", "end"]
		}
		
		lIndex = 0
		def raiser(s: str):raise dembParseException(f"Line {lIndex}: {s}")
		with open(path if path.endswith(".demb") else f"{path}.demb", 'r') as f:
			for line in f:
				lIndex+=1
				line = line.replace("\n","")
				while line.startswith("	") or line.startswith(" ") or line.startswith("    "):line = delStr(line)
				if line=="":continue
				if forceCreate or currentEmb == None:
					if not line.startswith("#") or line=="#" or line=="#end": raiser(f"You didn't provide a name")
					line = delStr(line)
					if line in self.parsed: raiser(f'Embed named "{line}" already exists')
					currentEmb = Embed(line) if currentEmb == None else currentEmb
					currentEmb.Name = line
					attrDict[Attribute.Undefined] = ["title", "comment", "description", "url", "color", "thumbnail", "footer"] if currentEmb.Name == "Default" else ["title", "comment", "description", "url", "field", "author", "color", "thumbnail", "footer"]
					forceCreate = False
					continue
				if line.startswith("@"):
					if line == "@": raiser("You didn't provide an attribute name")
					line = delStr(line)
					line = line.lower()
					if not line in attrDict[currentAttr]: raiser(f"The given attribute is not valid in this context")
					if line == "author":
						currentAttr=Attribute.Author
						currentInner = Author()
					elif line == "field":
						currentAttr=Attribute.Field
						currentInner = Field()
					elif line=="end":
						currentAttr=Attribute.Undefined
						if type(currentInner)==Field:currentEmb.Fields.append(currentInner)
						else:currentEmb.Author=currentInner
						currentAttrName = None
						currentInner = None
					else:currentAttrName=line
					continue
				if line.startswith("#"):
					if line.lower()!="#end": raiser("You can't create a new embed until you finish the current one")
					if currentAttr != Attribute.Undefined or currentAttrName!=None: raiser("Cannot end embed due to an unassigned attribute")
					self.parsed[currentEmb.Name] = currentEmb.Finalize()
					if currentEmb.Name == "Default":self.Default = deepcopy(currentEmb)
					currentEmb = None if self.Default == None else deepcopy(self.Default)
					currentAttr = Attribute.Undefined
					currentAttrName = None
					forceCreate = True
					continue
				if currentAttrName==None: raiser("There's no attribute you can set the value of")
				if line.startswith('"'):
					line = delStr(line)
				elif line.startswith("|"):
					templine = delStr(line)
					default = templine.split('=')
					if len(default)>1:
						templine = default[0]
						default = '='.join(default[1:])
					else:default = None
					line = kwargs[templine] if templine in kwargs else default if default!=None else templine
				if currentInner==None:
					Embed.GetMethod(f"set_{currentAttrName}").Invoke(currentEmb, [line])
				else:
					type(currentInner).GetMethod(f"set_{currentAttrName}").Invoke(currentInner, [line])
				currentAttrName = None
	def getEmbed(self, s: str, r = True, **kwargs):
		if kwargs!=self.defArgs:self.__init__(self.Path, **kwargs)
		if s in self.parsed: return self.parsed[s]
		if r:raise ValueError("Embed with the given name {0} doesn't exist".format(f'"{s}"'))
		return None
	def __call__(self, s: str, r = True, **kwargs):return self.getEmbed(s, r, **kwargs)
