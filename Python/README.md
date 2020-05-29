# Dependencies

[discord.py](https://pypi.org/project/discord.py/)

[ReflectionHelper](https://pypi.org/project/ReflectionHelper/)

# Example use

__example.demb__
```
#Default
	@color
		0x7222c9
#end

#Example Embed
	@title
		My fav embed
	@description
		It really is
	@field
		@name
			Love value
		@value
			|love
	@end
#end
```

__bot.py__
```py
from demb import Parser as ParserClass

Parser = new ParserClass("example.demb")

await ctx.channel.send(embed=Parser.getEmbed("Example Embed", love="High"))
```
![](https://cdn.discordapp.com/attachments/602891050494984195/715887409170087957/unknown.png)
