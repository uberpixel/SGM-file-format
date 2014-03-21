SGM and SGA File Formats
========================
---
####A lightweight game ready model and skeletal animation format specification and a blender exporter.
---
---
##SGM Specification

<pre><code>
############################################################
#Structure of exported mesh files (.sgm)
############################################################
#magic number - uint32 - 352658064
#version - uint8 - 3
#number of materials - uint8
#material id - uint8
#	number of uv sets - uint8
#		number of textures - uint8
#			texture type hint - uint8
#			filename length - uint16
#			filename - char*filename length
#	number of colors - uint8
#		color type hint - uint8
#		color rgba - float32*4
#
#number of meshs - uint8
#mesh id - uint8
#	used materials id - uint8
#	number of vertices - uint32
#	texcoord count - uint8
#	texdata count - uint8
#	has tangents - uint8 0 if not, 1 otherwise
#	has bones - uint8 0 if not, 1 otherwise
#	interleaved vertex data - float32
#		- position, normal, uvN, color, tangents, weights, bone indices
#
#	number of indices - uint32
#	index size - uint8, usually 2 or 4 bytes
#	indices - index size
#
#has animation - uint8 0 if not, 1 otherwise
#	animfilename length - uint16
#	animfilename - char*animfilename length
</code></pre>

---
##SGA Specification
<pre><code>
############################################################
#Structure of exported animation files (.sga)
############################################################
#magic number - uint32 - 383405658
#version - uint8 - 1
#skeleton name length - uint16
#skeleton name - char*skeleton name length
#
#number of bones - uint16
#	bone name length - uint16
#	bone name - char*bone name length
#	bone position xyz - float32*3
#	bone is a root (does not have a parent) - uint8 0 if not, 1 otherwise
#	bone number of children - uint16
#		child index within this list of bones - uint16
#
#number of animations - uint16
#	anim name length - uint16
#	anim name - char*anim name length
#	number of effected bones - uint16
#		skeleton bone id - uint16
#		number of frames for that bone - uint32
#			time - float
#			position xyz - 3*float
#			scale xyz - 3*float
#			rotation xyzw (quaternion) - 4*float
</code></pre>