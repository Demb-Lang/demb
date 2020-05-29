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

__bot.js__
```js
const ParserClass = require("./dembParser.js")

var Paraser = new ParserClass("example.demb")

message.channel.send(Parser.getEmbed("Example Embed", {
		love: "High"
	}))
```

![](https://cdn.discordapp.com/attachments/602891050494984195/715887409170087957/unknown.png)
