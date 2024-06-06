#################################
#Addon header
#################################
bl_info = {
	'name': 'Rayne model and animation formats (.sgm, .sga)',
	'author': 'Nils Daumann',
	'blender': (3, 0, 0),
	'version': (2, 1, 1),
	'description': 'Exports an object as .sgm file format and its animations as .sga file.',
	'category': 'Import-Export',
	'location': 'File -> Export -> Rayne Model (.sgm, .sga)'}

############################################################
#Structure of exported mesh files (.sgm)
############################################################
#magic number - uint32 - 352658064
#version - uint8 - 3
#number of materials - uint8
#   material id - uint8
#   number of uv sets - uint8
#   	number of textures - uint8
#   		texture type hint - uint8
#   		filename length - uint16
#   		filename - char*filename length
#   number of colors - uint8
#   	color type hint - uint8
#   	color rgba - float32*4
#
#number of meshs - uint8
#   mesh id - uint8
#   used materials id - uint8
#   number of vertices - uint32
#   texcoord count - uint8
#   color channel count - uint8 usually 0 or 4
#   has tangents - uint8 0 if not, 1 otherwise
#   has bones - uint8 0 if not, 1 otherwise
#   interleaved vertex data - float32
#   	- position, normal, uvN, color, tangents, weights, bone indices
#
#   number of indices - uint32
#   index size - uint8, usually 2 or 4 bytes
#   indices - index size
#
#has animation - uint8 0 if not, 1 otherwise
#   animfilename length - uint16
#   animfilename - char*animfilename length

############################################################
#Structure of exported animation files (.sga)
############################################################
#magic number - uint32 - 383405658
#version - uint8 - 1
#skeleton name length - uint16
#skeleton name - char*skeleton name length
#
#number of bones - uint16
#   bone name length - uint16
#   bone name - char*bone name length
#   bone position xyz - float32*3
#   bone is a root (does not have a parent) - uint8 0 if not, 1 otherwise
#   bone number of children - uint16
#   	child index within this list of bones - uint16
#
#number of animations - uint16
#   anim name length - uint16
#   anim name - char*anim name length
#   number of effected bones - uint16
#   	skeleton bone id - uint16
#   	number of frames for that bone - uint32
#   		time - float
#   		position xyz - 3*float
#   		scale xyz - 3*float
#   		rotation xyzw (quaternion) - 4*float

#################################
#Changelog
#################################
##V1 2011/10/22
#Features:
#-initial file format version 1
#-support for two uv sets
#-one texture per uv set, per vertex
#-different faces can have different textures, the object is automatically split into one mesh per texture
#-texture file ending can be chosen (textures have to be provided in the correct format for loading in iSDGE)
#-support for 4 vertex color channels (rgb and r from a second vertex color)
#-tangent generation and export
#-bone weights and per mesh indices with mapping to armature bones are exported
#-animation filename is exported
#-vertex data is exported interleaved with indices
#Known Problems:
#-every face has 3 vertices, which causes more vertex data then needed
##
#################################
##V1.1 2013/01/15
#-works with blender 2.6.5
#-fixed problem with vertices being exported for every face
#-number of indices is now 32bit, which solves problems with most larger meshs
#Known Problems:
#-crashes on exporting vertex colors
##
#################################
##V1.2 2013/03/05 - Version 1
#-added magic number
#-removed bone mapping
#-bone indices and weights are correctly exported
#-rest bones and animations can be exported
#-support for 32 bit indices -> flawed, the number of vertices is still a uint16
#Known Problems:
#-crashes on exporting vertex colors
#-scaled armatures and different origin of model and armature are problematic
##
#################################
##V1.3 2013/08/17 - Version 2
#-32bit indices are now fully supported -> number of vertices is now a uint32
#Known Problems:
#-crashes on exporting vertex colors
#-scaled armatures and different origin of model and armature are problematic
#-polygons other than tris aren´t working
##
#################################
##V1.4 2013/08/24
#-improved performance
#Known Problems:
#-crashes on exporting vertex colors
#-scaled armatures and different origin of model and armature are problematic
#-polygons other than tris aren´t working
#-texture and animation filenames currently only support ASCII encoding
##
#################################
##V1.4.1 2013/09/06
#-all strings stored in the format are now utf-8 encoded
#Known Problems:
#-crashes on exporting vertex colors
#-scaled armatures and different origin of model and armature are problematic
#-polygons other than tris aren´t working
##
#################################
##V1.5 2013/09/06
#-file format version 3
#-added support for material colors
#-textures are now assigned to correct uv coordinates
#Known Problems:
#-texture order may not fit to uv order...
#-crashes on exporting vertex colors?
#-scaled armatures and different origin of model and armature are problematic
##
#################################
##V1.5.1 2013/12/06
#-vertices are now correctly seperated for hard edges
#-texture usage hints are 0 for diffuse texture, 1 for normal maps and 2 for spec maps
#Known Problems:
#-texture order may not fit to uv order...
#-crashes on exporting vertex colors?
#-scaled armatures and different origin of model and armature are problematic
##
#################################
##V1.5.2 2014/03/21
#-updated to work with blender 2.70
#-fixed vertex color issue
#-fixed a problem with the export failing if a non image texture is attached to a material
#-as default tangent generation is now on
#Known Problems:
#-texture order may not fit to uv order...
#-scaled armatures and different origin of model and armature are problematic
##
#################################
##V1.5.3 2014/04/14
#-tangent generation is now ignored if there are no uv coordinates
#-renamed the menu item and description
#Known Problems:
#-texture order may not fit to uv order...
#-scaled armatures and different origin of model and armature are problematic
##
#################################
##V1.5.4 2019/05/18
#-added alternative texture format options (.astc, .dds, .* (* means exactly that and will be replaced by engine with preferred type for platform))
#Known Problems:
#-texture order may not fit to uv order...
#-scaled armatures and different origin of model and armature are problematic
##
#################################
##V1.5.5 2020/07/06
#-fixed a problem when not having a uv set
#-updated for blender 2.80.x
#Known Problems:
#-texture order may not fit to uv order...
#-scaled armatures and different origin of model and armature are problematic
##
#################################
##V1.6 2020/07/10
#-fixed color export
#-automatically apply object transformations to mesh
#Known Problems:
#-texture order may not fit uv order...
#-scaled armatures and different origin of model and armature are problematic
##
#################################
##V1.6.1 2020/07/28
#-can now export color AND texture if using mix node
#-hopefully fixed uvset export
#-color usage hints now match texture usage hints
#-base (0), specular (2), roughness (3) and emmision (4) colors are currently supported
#Known Problems:
#-texture order may not fit uv order...
#-scaled armatures and different origin of model and armature are problematic
##
#################################
##V1.6.2 2020/11/07
#-fixed two different diffuse colors getting exported
#Known Problems:
#-texture order may not fit uv order...
#-scaled armatures and different origin of model and armature are problematic
##
#################################
##V2.0.0 2020/03/12
#-added "Apply transforms" option which will automatically apply all transforms to the exported model, but makes it optional
#-added "Join objects" option which will automatically combine all selected objects into one exported model and ALWAYS applies all transforms
#-added support for exporting all selected objects into their own model file which will be called filename.objectname.sgm
#-sgm file extension is now automatically added if not specified by the user
#-added "Copy textures" option, which will save all textures referenced by the exported objects next to the files as png (currently it may change the textures color profile and other things based on the blender project setup)
#-added support for multiple textures per shader input (this allows for exporting lightmaps)
#-improved texture search, to find all textures used by a material, not just one that is directly connected
#Known Problems:
#-scaled armatures and different origin of model and armature are problematic
##
#################################
##V2.0.1 2020/06/12
#-fixed exporting materials using the RGB node
#-fixed exporting materials not using all uv sets
#-removed some debug logging
#Known Problems:
#-scaled armatures and different origin of model and armature are problematic
##
#################################
##V2.1.0 2022/09/07
#-made apply transforms option on by default
#-added apply modifiers option to automatically apply all modifiers to the exported object
#-requires Blender 3.x
#Known Problems:
#-scaled armatures and different origin of model and armature are problematic
##
#################################
##V2.1.1 2024/02/01
#-Animation export will now only export animations effecting the selected object.
#Known Problems:
#-scaled armatures and different origin of model and armature are problematic
##
#################################
##V2.1.2 2024/06/07
#-Messed around with gamma for vertex color export. Seems to better match the rendering in blender now.
#Known Problems:
#-scaled armatures and different origin of model and armature are problematic
##

#################################
#ToDO
#################################
#-automatically apply object transformations to armature
#-generation and export of shadow volume data, which otherwize is done on model loading in iSDGE
#-export of more complex material setups
#(-support for morph animations)



#################################
#Includes
#################################
import os
import bpy
import struct
import math
import mathutils
from mathutils import Matrix
from pathlib import Path

#Container classes for a better overview
class c_material(object):
	__slots__ = 'imagedict', 'colors', 'name'
	def __init__(self, name):
		self.imagedict = {}
		self.colors = []
		self.name = name

class c_vertex(object):
	__slots__ = 'blendindex', 'position', 'uvs', 'color', 'normal', 'tangent', 'weights', 'bones'
	def __init__(self, blendindex, position = (0, 0, 0), uvs = [], color = None, normal = (0, 0, 0), tangent = (0, 0, 0, 0), weights = (0, 0, 0, 0), bones = (0, 0, 0, 0)):
		self.blendindex = blendindex	#index within the blender mesh
		self.position = position
		self.uvs = uvs
		self.color = color
		self.normal = normal
		self.tangent = tangent
		self.weights = weights
		self.bones = bones

	def getTuple(self):
		position = tuple(self.position)
		uvs = tuple(self.uvs)
		color = (-1, -1, -1, -1)
		if self.color != None:
			color = tuple(self.color)
		normal = tuple(self.normal)
		weights = tuple(self.weights)
		bones = tuple(self.bones)
		return (position, uvs, color, normal, weights, bones)

class c_triangle(object):
	__slots__ = 'vertices', 'material', 'newindices'
	def __init__(self, vertices = [], material = 0, newindices = None):
		self.vertices = vertices
		self.material = material
		self.newindices = newindices		#indices within the c_mesh
		
class c_mesh(object):
	__slots__ = 'triangles', 'material', 'vertices', 'indices'
	def __init__(self, material = 0, tri = None):
		self.vertices = []
		self.triangles = []
		if tri != None:
			self.triangles.append(tri)
		self.material = material
		self.indices = []
	
	#duplicates face vertices with different uv coords and sets the new index
	def uvsplit(self):
		inddict = {}
		for tri in self.triangles:
			ind = []
			for trivert in tri.vertices:
				verttuple = trivert.getTuple()
				if verttuple in inddict:
					ind.append(inddict[verttuple])
				else:
					ind.append(len(self.vertices))
					inddict[verttuple] = len(self.vertices)
					self.vertices.append(trivert)
			
			self.indices.append(ind[0])
			self.indices.append(ind[1])
			self.indices.append(ind[2])
	
	#generates tangent for the given face
	def genfacetangent(self, vertex, neighbour_a, neighbour_b, bitangent0, bitangent1, bitangent2):
		posdir1 = (neighbour_a.position[0]-vertex.position[0], neighbour_a.position[1]-vertex.position[1], neighbour_a.position[2]-vertex.position[2])
		posdir2 = (neighbour_b.position[0]-vertex.position[0], neighbour_b.position[1]-vertex.position[1], neighbour_b.position[2]-vertex.position[2])
		uvdir1 = (neighbour_a.uvs[0][0]-vertex.uvs[0][0], neighbour_a.uvs[0][1]-vertex.uvs[0][1])
		uvdir2 = (neighbour_b.uvs[0][0]-vertex.uvs[0][0], neighbour_b.uvs[0][1]-vertex.uvs[0][1])
		
		r = (uvdir1[0]*uvdir2[1]-uvdir2[0]*uvdir1[1])
		if r != 0:
			r = 1.0/r
		else:
			r = 1.0
		tangent = ((uvdir2[1]*posdir1[0]-uvdir1[1]*posdir2[0])*r, (uvdir2[1]*posdir1[1]-uvdir1[1]*posdir2[1])*r, (uvdir2[1]*posdir1[2]-uvdir1[1]*posdir2[2])*r, 0.0)
		bitangent = ((uvdir1[0]*posdir2[0]-uvdir2[0]*posdir1[0])*r, (uvdir1[0]*posdir2[1]-uvdir2[0]*posdir1[1])*r, (uvdir1[0]*posdir2[2]-uvdir2[0]*posdir1[2])*r)
		
		vertex.tangent = (vertex.tangent[0]+tangent[0], vertex.tangent[1]+tangent[1], vertex.tangent[2]+tangent[2], 0.0)
		neighbour_a.tangent = (neighbour_a.tangent[0]+tangent[0], neighbour_a.tangent[1]+tangent[1], neighbour_a.tangent[2]+tangent[2], 0.0)
		neighbour_b.tangent = (neighbour_b.tangent[0]+tangent[0], neighbour_b.tangent[1]+tangent[1], neighbour_b.tangent[2]+tangent[2], 0.0)
		
		bitangent0 = (bitangent0[0]+bitangent[0], bitangent0[1]+bitangent[1], bitangent0[2]+bitangent[2])
		bitangent1 = (bitangent1[0]+bitangent[0], bitangent1[1]+bitangent[1], bitangent1[2]+bitangent[2])
		bitangent2 = (bitangent2[0]+bitangent[0], bitangent2[1]+bitangent[1], bitangent2[2]+bitangent[2])
		return bitangent0, bitangent1, bitangent2
	
	#generates tangents
	def gentangents(self):
		i = 0
		bitangents = []
		while i < len(self.vertices):
			bitangents.append((0, 0, 0))
			i += 1
		
		#Calculate the tangent of each vertex
		i = 0
		while i < len(self.indices):
			bitangents[self.indices[i]], bitangents[self.indices[i+2]], bitangents[self.indices[i+1]] = self.genfacetangent(self.vertices[self.indices[i]], self.vertices[self.indices[i+2]], self.vertices[self.indices[i+1]], bitangents[self.indices[i]], bitangents[self.indices[i+2]], bitangents[self.indices[i+1]])
			i += 3
		
		#Normalize all tangents
		i = 0
		while i < len(self.vertices):
			temptangent = (self.vertices[i].tangent[0]-self.vertices[i].normal[0]*self.vertices[i].normal[0]*self.vertices[i].tangent[0], self.vertices[i].tangent[1]-self.vertices[i].normal[1]*self.vertices[i].normal[1]*self.vertices[i].tangent[1], self.vertices[i].tangent[2]-self.vertices[i].normal[2]*self.vertices[i].normal[2]*self.vertices[i].tangent[2], 0.0)
			l = temptangent[0]*temptangent[0]+temptangent[1]*temptangent[1]+temptangent[2]*temptangent[2]
			l = math.sqrt(l)
			if l == 0: l = 1
			temptangent = (temptangent[0]/l, temptangent[1]/l, temptangent[2]/l, 0.0)
			self.vertices[i].tangent = temptangent
			i += 1
			
		#Calculate bitangent direction
		i = 0
		while i < len(self.vertices):
			temptangent = self.vertices[i].tangent
			bicross = (self.vertices[i].normal[1]*temptangent[2]-self.vertices[i].normal[2]*temptangent[1], self.vertices[i].normal[2]*temptangent[0]-self.vertices[i].normal[0]*temptangent[2], self.vertices[i].normal[0]*temptangent[1]-self.vertices[i].normal[1]*temptangent[0])
			bidot = bicross[0]*bitangents[i][0]+bicross[1]*bitangents[i][1]+bicross[2]*bitangents[i][2]
			if bidot < 0.0:
				bidot = -1.0
			else:
				bidot = 1.0
			self.vertices[i].tangent = (temptangent[0], temptangent[1], temptangent[2], bidot)
			i += 1


class c_object(object):
	__slots__ = 'meshs', 'hasbones', 'animname'
	#splits the blender object into triangle meshs with the same textures
	def __init__(self, objects, exptangents, texextension, applytransforms, applymodifiers, copytextures):
		
		self.hasbones = False
		#check for bones, only supported when exporting a single object, ignore otherwise
		if len(objects) == 1:
			ArmatureList = [Modifier for Modifier in objects[0].modifiers if Modifier.type == "ARMATURE"]
			if ArmatureList:
				self.hasbones = True
			if len(ArmatureList) > 1:
				print("only one armature per object supported: possible messed up bone assignements")
		
		materials = []
		triangles = []
		materialmapping = {}
		materialoffset = 0
		for object in objects:
			#apply object transforms
			dg = bpy.context.evaluated_depsgraph_get()
			obj = object.evaluated_get(dg)
			objectdata = obj.to_mesh(preserve_all_data_layers=True, depsgraph=dg)
			#objectdata = object.to_mesh(scene = bpy.context.scene, apply_modifiers = applymodifiers, settings = 'PREVIEW') # object.data.copy()
			if applytransforms:
				objectdata.transform(obj.matrix_world)

			#generate list of the objects materials
			for i, mat in enumerate(objectdata.materials):
				foundmaterial = False
				for n, existingmaterial in enumerate(materials):
					if existingmaterial.name == mat.name:
						materialmapping[materialoffset + i] = n
						foundmaterial = True
						break
				if foundmaterial:
					continue
				
				material = c_material(mat.name)
				materialmapping[materialoffset + i] = len(materials)
				if mat.use_nodes and mat.node_tree:
					for node in mat.node_tree.nodes:
						if node.bl_idname.startswith('ShaderNodeBsdf'):
							for colorInput in node.inputs:
								usageHint = 0
								wantsColor = True
								if colorInput.identifier == 'Base Color':
									usageHint = 0
								elif colorInput.identifier == 'Specular':
									usageHint = 2
								elif colorInput.identifier == 'Roughness':
									usageHint = 3
								elif colorInput.identifier == 'Emission':
									usageHint = 4
								elif colorInput.identifier == 'Normal':   
									usageHint = 1
									wantsColor = False
								else:
									continue
								
								shaderInputs = self.get_shader_input(colorInput, objectdata, [])
								print(shaderInputs)
								for input in shaderInputs:
									if input[0] == "COLOR" and wantsColor:
										material.colors.append((input[1], usageHint))
									if input[0] == "TEXTURE":
										uvlayer = input[1]
										if not uvlayer in material.imagedict:
											material.imagedict[uvlayer] = []
										img = input[2]
										if texextension != 'keep':
											img = img[:-3]
											img += texextension
										material.imagedict[uvlayer].append((img, usageHint, input[3]))
							break

				else:
					if mat.blend_method != 'OPAQUE':
						material.colors.append(((mat.diffuse_color[0], mat.diffuse_color[1], mat.diffuse_color[2], mat.alpha), 0))
					else:
						material.colors.append(((mat.diffuse_color[0], mat.diffuse_color[1], mat.diffuse_color[2], 1.0), 0))
						
				materials.append(material)

			objectdata.calc_loop_triangles()
			#generate vertices and triangles
			for triangle in objectdata.loop_triangles:
				verts = []
				for n, vertind in enumerate(triangle.vertices):
					uvs = []
					for uv_layer in objectdata.uv_layers:
						loopIndex = triangle.loops[n]
						uvs.append((round(uv_layer.data[loopIndex].uv[0], 6), 1.0-round(uv_layer.data[loopIndex].uv[1], 6)))
					
					color = None
					for color_layer in objectdata.vertex_colors:
						loopIndex = triangle.loops[n]
						colorArray = color_layer.data[loopIndex].color
						color = (pow(colorArray[0], 2.2), pow(colorArray[1], 2.2), pow(colorArray[2], 2.2), pow(colorArray[3], 2.2))
					
					position = (objectdata.vertices[vertind].co.x, objectdata.vertices[vertind].co.y, objectdata.vertices[vertind].co.z)
					normal = (triangle.split_normals[n][0], triangle.split_normals[n][1], triangle.split_normals[n][2])

					#get vertex weights and bone indices
					weights = [0, 0, 0, 0]
					bones = [0, 0, 0, 0]
					if self.hasbones == True:
						groups = sorted(objectdata.vertices[vertind].groups, key=lambda item: item.weight, reverse=True)

						sumweights = 0
						for g, group in enumerate(groups):
							if g > 3:
								break
							sumweights += group.weight

						for g, group in enumerate(groups):
							if g > 3:
								print("more then four groups assigned to vertex: loss of data")
								break
							weights[g] = group.weight/sumweights
							bones[g] = ArmatureList[0].object.data.bones.find(obj.vertex_groups[group.group].name)
				
					verts.append(c_vertex(vertind, position, uvs, color, normal))
					verts[-1].weights = weights #hacky as the above line should already do this, but for some reason does not...
					verts[-1].bones = bones
				
				realmaterialindex = materialmapping[materialoffset + triangle.material_index]
				material = materials[realmaterialindex]
				triangles.append(c_triangle(verts, material))
				
			materialoffset += len(objectdata.materials)

			obj.to_mesh_clear()
		
		#generate meshs
		self.meshs = []
		m = c_mesh(triangles[0].material)
		self.meshs.append(m)
		for tri in triangles:
			check = 0
			for mesh in self.meshs:
				if mesh.material == tri.material:
					mesh.triangles.append(tri)
					check = 1
					break
			if check == 0:
				m = c_mesh(tri.material, tri)
				self.meshs.append(m)
		
		for mesh in self.meshs:
			mesh.uvsplit()
		
		if exptangents == True and len(material.imagedict) > 0:
			for mesh in self.meshs:
				mesh.gentangents()
	
	
	def write(self, filename, exptextures, exptangents, expanimations):
		print("open or create file")
		file = open(filename, 'wb')

		file.write(struct.pack('<L', 352658064))
		print("write file format version number: 3")
		file.write(struct.pack('<B', 3))

		print("write materials")
		file.write(struct.pack('<B', len(self.meshs)))  #number of materials
		for i, mesh in enumerate(self.meshs):
			file.write(struct.pack('<B', i))			#material id
			if exptextures != True:
				file.write(struct.pack('<B', 0))	#uvcount
			else:
				numuvs = 0
				for uv in mesh.material.imagedict:
					if uv >= numuvs:
						numuvs = uv + 1
				file.write(struct.pack('<B', numuvs)) #uvcount
				for uv in range(0, numuvs):
					numimgs = 0
					if uv in mesh.material.imagedict:
						numimgs = len(mesh.material.imagedict[uv])
					file.write(struct.pack('<B', numimgs)) #imagecount
					if numimgs > 0:
						for img in mesh.material.imagedict[uv]:
							file.write(struct.pack('<B', img[1])) #usage hint
							texname = img[0].encode("utf_8")
							file.write(struct.pack('<H', len(texname)+1))
							file.write(struct.pack('<%is'%(len(texname)+1), texname))

			numcols = len(mesh.material.colors)
			file.write(struct.pack('<B', numcols)) #number of colors
			for col in mesh.material.colors:
				file.write(struct.pack('<B', col[1]))
				bindata = struct.pack('<ffff', col[0][0], col[0][1], col[0][2], col[0][3])
				file.write(bindata)

		print("write meshs")
		file.write(struct.pack('<B', len(self.meshs)))
		for i, mesh in enumerate(self.meshs):
			datachannels = 0
			if mesh.vertices[0].color != None:
				datachannels = 4
				
			file.write(struct.pack('<B', i))	#mesh id
			file.write(struct.pack('<B', i))	#material id
			file.write(struct.pack('<I', len(mesh.vertices)))   #vertexnum
			file.write(struct.pack('<B', len(mesh.material.imagedict))) #texcoord count
			file.write(struct.pack('<B', datachannels)) #texdata count
			
			if exptangents == True:
				file.write(struct.pack('<B', 1)) #has tangents
			else:
				file.write(struct.pack('<B', 0)) #does not have tangents
				
			if self.hasbones == True:
				file.write(struct.pack('<B', 1)) #has bones
			else:
				file.write(struct.pack('<B', 0)) #does not have bones (number of bones is 0)
			
			print("write interleaved vertex data")
			
			for vertex in mesh.vertices:
				bindata = struct.pack('<fff', -vertex.position[0], vertex.position[2], vertex.position[1])
				file.write(bindata)
				
				bindata = struct.pack('<fff', -vertex.normal[0], vertex.normal[2], vertex.normal[1])
				file.write(bindata)

				set = 0
				while set < len(mesh.material.imagedict):
					bindata = struct.pack('<ff', vertex.uvs[set][0], vertex.uvs[set][1])
					file.write(bindata)
					set += 1
				
				if mesh.vertices[0].color != None:
					bindata = struct.pack('<ffff', vertex.color[0], vertex.color[1], vertex.color[2], vertex.color[3])
					file.write(bindata)
				
				if exptangents == True:
					bindata = struct.pack('<ffff', -vertex.tangent[0], vertex.tangent[2], vertex.tangent[1], vertex.tangent[3])
					file.write(bindata)
					
				if self.hasbones == True:
					bindata = struct.pack('<ffff', vertex.weights[0], vertex.weights[1], vertex.weights[2], vertex.weights[3])
					file.write(bindata)
					bindata = struct.pack('<ffff', vertex.bones[0], vertex.bones[1], vertex.bones[2], vertex.bones[3])
					file.write(bindata)
					
			print("finished writing interleaved vertex data")
			
			print("write indices")
			file.write(struct.pack('<I', len(mesh.indices)))
			maxval = max(mesh.indices)
			if maxval > 65535:
				file.write(struct.pack('<B', 4))
			else:
				file.write(struct.pack('<B', 2))

			for ind in mesh.indices:
				if maxval > 65535:
					bindata = struct.pack('<I', ind)
				else:
					bindata = struct.pack('<H', ind)
				file.write(bindata)
				
		print("write animation reference")
		if self.hasbones == True and expanimations == True:
			file.write(struct.pack('<B', 1)) #has animations
			animfile = self.animname.encode('utf_8')
			file.write(struct.pack('<H', len(animfile)+1))
			file.write(struct.pack('<%is'%(len(animfile)+1), animfile))
		else:
			file.write(struct.pack('<B', 0)) #does not have animations
	
		file.close()
		
		
	def copy_textures(self, filename):
		for i, mesh in enumerate(self.meshs):
			numuvs = len(mesh.material.imagedict)
			for uv in range(0, numuvs):
				for img in mesh.material.imagedict[uv]:
					path = Path(filename)
					path = path.parent.joinpath(img[0])
					if path.suffix == ".*":
						path = path.with_suffix(".png")
					if not path.exists():
						img[2].save_render(str(path.resolve()))
						
	
	def get_shader_input(self, input, objectdata, inputs = []):
		if not input.is_linked:
			if input.type == 'RGBA':
				inputs.append(('COLOR', input.default_value))
				print(input.default_value)
			return inputs
		
		shaderNode = input.links[0].from_node
		
		if shaderNode.bl_idname == 'ShaderNodeRGB':
			inputs.append(('COLOR', shaderNode.outputs[0].default_value))
			print(shaderNode.color)
			return inputs
		
		if shaderNode.bl_idname == 'ShaderNodeTexImage':
			if not shaderNode.image:
				return inputs
			
			imgpath = shaderNode.image.filepath
			img = imgpath.split('/')
			img = img[len(img)-1]
			img = img.split('\\')
			img = img[len(img)-1]
				
			uvlayer = 0
			isValidUVLayer = False
			for newInput in shaderNode.inputs:
				if not newInput.is_linked:
					continue
				if newInput.identifier != 'Vector':
					continue
				for link in newInput.links:
					if link.from_node.bl_idname != 'ShaderNodeUVMap':
						continue
					uvlayer = objectdata.uv_layers.find(link.from_node.uv_map)
					if uvlayer < 0:
						uvlayer = 0
					isValidUVLayer = True
					break
				if isValidUVLayer == True:
					break
					
			inputs.append(("TEXTURE", uvlayer, img, shaderNode.image))
			return inputs
		
		for newInput in shaderNode.inputs:
			self.get_shader_input(newInput, objectdata, inputs)
			
		return inputs


class c_boneframe(object):
	__slots__ = 'time', 'position', 'scale', 'rotation'
	def __init__(self, time, position, scale, rotation):
		self.time = time
		self.position = position
		self.scale = scale
		self.rotation = rotation

class c_animation(object):
	__slots__ = 'name', 'length', 'frames'
	def __init__(self, name):
		self.name = name
		self.frames = {}

class c_bone(object):
	__slots__ = 'name', 'children', 'position', 'isroot'
	def __init__(self, name, position, isroot):
		self.name = name
		self.children = []
		self.position = position
		self.isroot = isroot;


class c_armature(object):
	__slots__ = 'name', 'bones', 'animations'
	def __init__(self, objparent):
		self.name = 'empty'
		self.bones = []
		self.animations = []

		ArmatureList = [Modifier for Modifier in objparent.modifiers if Modifier.type == "ARMATURE"]
		if ArmatureList:
			self.name = ArmatureList[0].object.data.name
		else:
			return
		armatureObject = ArmatureList[0].object

		animationData = armatureObject.animation_data
		if not animationData:
			return

		#apply object transforms
		armatureRest = armatureObject.data #.copy()
		#armatureRest.transform(armatureObject.matrix_world)

		#get skeleton data
		for bone in armatureRest.bones:
			b = c_bone(bone.name, bone.head_local, False if bone.parent else True)  #add bone
			for child in bone.children:
				b.children.append(armatureRest.bones.find(child.name))
			self.bones.append(b)

		vertspacemat = mathutils.Matrix.Identity(4)
		vertspacemat[0][0] = -1
		vertspacemat[1][1] = 0
		vertspacemat[1][2] = 1
		vertspacemat[2][2] = 0
		vertspacemat[2][1] = 1

		animationActions = []
		if animationData.action:
			animationActions.append(animationData.action)
		for track in animationData.nla_tracks:
			for strip in track.strips:
				animationActions.append(strip.action)

		#get animation frames
		frame_current = bpy.context.scene.frame_current
		for action in animationActions:
			print("collecting animation action: " + action.name)
			armatureObject.animation_data.action = action
			anim = c_animation(action.name)
			for frame in range(int(action.frame_range[0]), int(action.frame_range[1])):
				bpy.context.scene.frame_set(frame)
				for i, bone in enumerate(armatureObject.pose.bones):
					index = armatureRest.bones.find(bone.bone.name)
					
					trans = Matrix.Translation(vertspacemat @ bone.bone.head_local)
					itrans = Matrix.Translation(vertspacemat @ (-bone.bone.head_local))
					if bone.parent:
						mat_final = itrans @ vertspacemat @ bone.parent.bone.matrix_local @ (vertspacemat @ bone.parent.matrix).inverted() @ vertspacemat @ bone.matrix @ (vertspacemat @ bone.bone.matrix_local).inverted() @ trans
					else:
						mat_final = itrans @ vertspacemat @ bone.matrix @ (vertspacemat @ bone.bone.matrix_local).inverted() @ trans
					pos, rot, scal = mat_final.decompose()

					rot = (rot[1], rot[2], rot[3], rot[0])
					boneframe = c_boneframe(frame-action.frame_range[0], pos, scal, rot)
					if frame == action.frame_range[0]:
						anim.frames[index] = []
					(anim.frames[index]).append(boneframe)

			self.animations.append(anim)
		bpy.context.scene.frame_set(frame_current)


	def write(self, filename):
		"""
		file = open(filename, 'w')
		file.write(self.name+"\n")
		file.write("\nskeleton:")
		for bone in self.bones:
			file.write(bone.name+"\n")
			file.write("pos: %f %f %f\n" % (-bone.position[0], bone.position[2], bone.position[1]))
			file.write("child count: %i children:" % len(bone.children))
			for child in bone.children:
				file.write("%i " % child)
			file.write("\n")

		file.write("\nanimations:\n")
		file.write("count: %i\n" % len(self.animations))
		for anim in self.animations:
			file.write("name: "+anim.name+"\n")
			file.write("bone count: %i\n" % len(anim.frames))
			for i, boneframes in anim.frames.items():
				file.write("skeleton bone id: %i\n" % i)
				file.write("bone frame count: %i\n" % len(boneframes))
				for frame in boneframes:
					file.write("time: %f\n" % frame.time)
					file.write("pos: %f %f %f\n" % (-frame.position[0], frame.position[2], frame.position[1]))
					file.write("scale: %f %f %f\n" % (frame.scale[0], frame.scale[2], frame.scale[1]))
					file.write("rot: %f %f %f %f\n" % (frame.rotation[0], frame.rotation[1], frame.rotation[2], frame.rotation[3]))
					#print(frame.rotation)
		file.close()
		"""
		file = open(filename, 'wb')
		file.write(struct.pack('<L', 383405658))	#magic number
		file.write(struct.pack('<B', 1))	#file type version (1)
		skeletonname = self.name.encode('utf_8')
		file.write(struct.pack('<H', len(skeletonname)+1))
		file.write(struct.pack('<%is'%(len(skeletonname)+1), skeletonname))
		file.write(struct.pack('<H', len(self.bones)))
		for bone in self.bones:
			bonename = bone.name.encode('utf_8')
			file.write(struct.pack('<H', len(bonename)+1))
			file.write(struct.pack('<%is'%(len(bonename)+1), bonename))
			bindata = struct.pack('<fff', -bone.position[0], bone.position[2], bone.position[1])
			file.write(bindata)
			file.write(struct.pack('<B', 1 if bone.isroot else 0))
			file.write(struct.pack('<H', len(bone.children)))
			for child in bone.children:
				file.write(struct.pack('<H', child))

		file.write(struct.pack('<H', len(self.animations)))
		for anim in self.animations:
			animname = anim.name.encode('utf_8')
			file.write(struct.pack('<H', len(animname)+1))
			file.write(struct.pack('<%is'%(len(animname)+1), animname))
			file.write(struct.pack('<H', len(anim.frames)))
			for i, boneframes in anim.frames.items():
				file.write(struct.pack('<H', i))
				file.write(struct.pack('<L', len(boneframes)))
				for frame in boneframes:
					file.write(struct.pack('<f', frame.time))
					bindata = struct.pack('<fff', frame.position[0], frame.position[1], frame.position[2])
					file.write(bindata)
					bindata = struct.pack('<fff', frame.scale[0], frame.scale[1], frame.scale[2])
					file.write(bindata)
					bindata = struct.pack('<ffff', frame.rotation[0], frame.rotation[1], frame.rotation[2], frame.rotation[3])
					file.write(bindata)
		file.close()


#################################
#Interface and stuff
#################################
from bpy.props import *
class ExportSGM(bpy.types.Operator):
	'''Export to Rayne model file format (.sgm)'''
	bl_idname = "export.rayne_sgm"
	bl_label = 'Export Rayne Model'

	filepath : StringProperty(name="File Path", description="Filepath used for exporting the Rayne model file", maxlen= 1024, default= "")
	check_existing : BoolProperty(name="Check Existing", description="Check and warn on overwriting existing files", default=True, options={'HIDDEN'})
	
	#properties
	exptextures : BoolProperty(name="Export textures", description="Reference external image files to be used by the model.", default=True)
	texextension : EnumProperty(
			name="Texture extension",
			items=(('png', ".png", ""),
				   ('*', "flexible", ""),
				   ('keep', "keep current", ""),
				   ),
			default='*',
			)
	exptangents : BoolProperty(name="Export tangents", description="Generate tangents for the model to use for example tangent space normal mapping.", default=True)
	expanimations : BoolProperty(name="Export animations", description="Export animation data in an additional file and reference it in the object.", default=True)
	applytransforms : BoolProperty(name="Apply transforms", description="Apply all object transforms, making the exported object origin equal to the blender world origin.", default=True)
	applymodifiers : BoolProperty(name="Apply modifiers", description="Apply all object modifiers with preview settings.", default=True)
	joinobjects : BoolProperty(name="Join objects", description="Joins all selected objects into one. This will automatically apply the transform if more than one object is selected. This will ignore armatures!", default=False)
	copytextures : BoolProperty(name="Copy textures", description="Copy all textures used by the exported objects materials into the same folder as the exported file. This will convert to png if png of flexible format is exported. It will NOT overwrite existing files.", default=False)
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode='OBJECT')
		print("start exporting .sgm file")
		
		if not self.filepath.endswith(".sgm"):
			self.filepath += ".sgm"
		
		didjoinobjects = False
		if self.joinobjects and len(context.selected_objects) > 1:
			obj = c_object(context.selected_objects, self.exptangents, self.texextension, True, self.copytextures)
			obj.write(self.filepath, self.exptextures, self.exptangents, False)
			if self.copytextures and self.exptextures:
				obj.copy_textures(self.filepath)
		else:
			for object in context.selected_objects:
				path = Path(self.filepath)
				if len(context.selected_objects) > 1:
					path = path.with_suffix("." + object.name + ".sgm")
				actualfilepath = str(path)
				print(actualfilepath)
				obj = c_object([object], self.exptangents, self.texextension, self.applytransforms, self.applymodifiers, self.copytextures)
				obj.animname = os.path.basename(actualfilepath[0:len(actualfilepath)-4]+".sga")
				obj.write(actualfilepath, self.exptextures, self.exptangents, self.expanimations)
				if self.copytextures and self.exptextures:
					obj.copy_textures(self.filepath)
				print("finished exporting .sgm file")
				if obj.hasbones and self.expanimations:
					print("start exporting .sga file")
					arm = c_armature(context.object)
					arm.write(actualfilepath[0:len(actualfilepath)-4]+".sga")
					print("finished exporting .sga file")
			
		return {'FINISHED'}

	def invoke(self, context, event):
		wm = context.window_manager
		wm.fileselect_add(self)
		return {'RUNNING_MODAL'}


def menu_func_export(self, context):
	default_path = os.path.splitext(bpy.data.filepath)[0] + ".sgm"
	self.layout.operator(ExportSGM.bl_idname, text="Rayne Model (.sgm)").filepath = default_path


def register():
	bpy.utils.register_class(ExportSGM)
	bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
	
def unregister():
	bpy.utils.unregister_class(ExportSGM)
	bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
	
if __name__ == "__main__":
	register()
