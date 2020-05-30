Demb is an easy to use custom Discord embed system.

# Syntax

File extension: `demb`

```
#Embed name
	@root attribuite
		value
		
	@attribute group
		@child attribute
			value
	@end
#end
```

*1 file can have more than one embeds, but with different names each*

# Global attributes*

These attributes can be used anywhere inside an embed

| Attribute name | Description |
|-|-|
|Comment|Doesn't do anything, you can use this to comment your demb file|

# Root Attributes*

These attributes can be used inside an embed outside an attribute group

| Attribute name | Description |
|-|-|
|Title|The title of the embed|
|Description|The description of the embed|
|URL|URL of title|
|Color|The color of the embed (hex, format: `0x<values>`)|
|Thumbnail|A small image in the top-right corner (URL)|
|Footer|Bottom text of the embed|

# Attribute groups

__Global group attributes__*

| Attribute name | Description |
|-|-|
| end | Represents the end of the group |

## Field

Represents a field in the embed

| Child attribute name | Description |
|-|-|
| Name | The name of the field |
| Value | The value of the field |
| Inline | `true` or `false` - can be shown next to the field before/after |

## Author

Represents the author of the embed

| Child attribute name | Description |
|-|-|
| Name | The name of the author |
| URL | URL reference to the author |
| Icon_URL | Avatar of the author |

# Default embed

If you name the embed `Default`, only the Global and Root attributes can be used in it, and those values will be the values of the attributes in every embed that doesn't have that attribute.

*This embed should be placed above the ones you'd like to apply it on*

```
#Default
	@footer
		Default footer
#end

#Example
	@title
		Example embed
	
	@comment
		This embed has a footer of a value "Default footer"
#end
```

# Value syntax

Normally values are normal texts

```
@attribute
	value

@comment
	The value of the attribute above is "value"
```

Values can have `|` (variable) and `"` (raw) characters as first characters.

### Variable

The value is the name of the variable the embed will search for.

These can be assigned when creating a Parser object or querying an embed. (Examples in language folders)

These variables can have default values separated by `=`

*Example*:
`|variable=default`

If there's no default value, nor an assigned value the value will be the name of the variable, unless the attribute is `color` or `inline` in which case `color` will be `0x000000` and `inline` will be `false`.

### Raw

The text after the `"` symbol will be the value of the attribute.

This can be used if you want the `|` sign: `"|text`

Or if you want an empty text: `"`
<br>
<br>
<br>
<br>
<br>
<br>
*The list of attributes may incrase
