# encoding: utf-8


import networkx as nx
import matplotlib.pyplot as plt


def search(g, origin, destiny, checked=None, jumps=0, path='', options=''):
	if checked is None:
		checked = []

	if origin == destiny:
		path += '%s' % origin
		options = [jumps, path]
	elif destiny in g.neighbors(origin):
		jumps += 1
		path += '%s ---- %s' % (origin, destiny)
		options = [jumps, path]
	else:
		jumps += 1
		path += '%s ---- ' % origin
		checked.append(origin)
		c = checked[:]
		for adjacent in g.neighbors(origin):
			if adjacent not in checked:
				option = search(g, adjacent, destiny, checked, jumps, path, options)
				if options != '':
					if option is not None and option[0] < options[0]:
						options = option
				else:
					options = option
				checked = c
	return options


def coordinate(g):
	pos = {}
	pos['AC'] = [3.610, 21.773]
	pos['AL'] = [24.535, 21.265]
	pos['AM'] = [6.525, 27.102]
	pos['AP'] = [12.766, 33.339]
	pos['BA'] = [20.210, 18.771]
	pos['CE'] = [23.072, 28.217]
	pos['ES'] = [21.438, 13.169]
	pos['GO'] = [15.554, 15.979]
	pos['MA'] = [17.003, 28.930]
	pos['MG'] = [19.438, 12.931]
	pos['MS'] = [13.646, 10.043]
	pos['MT'] = [11.597, 18.096]
	pos['PA'] = [12.654, 29.056]
	pos['PB'] = [25.863, 26.015]
	pos['PE'] = [24.485, 24.565]
	pos['PI'] = [19.640, 26.439]
	pos['PR'] = [16.273, 5.428]
	pos['RJ'] = [21.057, 10.253]
	pos['RN'] = [25.409, 28.905]
	pos['RO'] = [7.404, 20.062]
	pos['RR'] = [5.473, 32.320]
	pos['RS'] = [13.030, -1.325]
	pos['SC'] = [15.049, 1.797]
	pos['SE'] = [23.272, 19.411]
	pos['SP'] = [18.036, 8.047]
	pos['TO'] = [15.454, 23.013]

	return pos


def generateGraph(g, origin, destiny, path):
	nodes = g.nodes()
	edges = g.edges()
	labels = {}

	# Creat nodes
	for node in nodes:
		# Writing labels
		labels[node] = '%s' % node
		g[node]['color'] = '#e0e0e0'
		g[node]['size'] = 300
		if node == origin or node == destiny:
			g[node]['color'] = '#A82424'
			g[node]['size']  = 500

	# Creat edges
	for edge in edges:
		g[edge[0]][edge[1]]['color'] = '#000000'
		g[edge[0]][edge[1]]['weight'] = 1.5

	i = 0
	while i < len(path) - 1:
		g[path[i]][path[i + 1]]['color'] = '#A82424'
		g[path[i]][path[i + 1]]['weight'] = 3
		if i > 0:
			g[path[i]]['color'] = '#6868B0'
		i += 1

	pos = coordinate(g)

	# Nodes' attributes
	colorsNode = [g[u]['color'] for u in nodes]
	sizesNode = [g[u]['size'] for u in nodes]
	# Edges' attributes
	colorsEdge = [g[u][v]['color'] for u, v in edges]
	weightsEdge = [g[u][v]['weight'] for u, v in edges]

	# Drawing the network
	nx.draw_networkx_nodes(g, pos, nodelist=nodes, node_color=colorsNode, node_size=sizesNode)
	nx.draw_networkx_edges(g, pos, edgelist=edges, edge_color=colorsEdge, width=weightsEdge)
	nx.draw_networkx_labels(g, pos, labels, font_size=12)
	plt.show()


def main():
	# -------------------- VARIABLES INIATIALIZATION -------------------- #
	# All brazilian states' frontiers
	edges = [
		('AC', 'AM'), ('AC', 'RO'), ('AL', 'BA'), ('AL', 'PE'), ('AL', 'SE'), ('AM', 'MT'), ('AM', 'PA'), ('AM', 'RO'),
		('AM', 'RR'), ('AP', 'PA'), ('BA', 'ES'), ('BA', 'GO'), ('BA', 'MG'), ('BA', 'PE'), ('BA', 'PI'), ('BA', 'SE'),
		('BA', 'TO'), ('CE', 'PB'), ('CE', 'PE'), ('CE', 'PI'), ('CE', 'RN'), ('ES', 'MG'), ('ES', 'RJ'), ('GO', 'MG'),
		('GO', 'MS'), ('GO', 'MT'), ('GO', 'TO'), ('MA', 'PA'), ('MA', 'PI'), ('MA', 'TO'), ('MG', 'MS'), ('MG', 'RJ'),
		('MG', 'SP'), ('MS', 'MT'), ('MS', 'PR'), ('MS', 'SP'), ('MT', 'PA'), ('MT', 'RO'), ('MT', 'TO'), ('PA', 'RR'),
		('PA', 'TO'), ('PB', 'PE'), ('PB', 'RN'), ('PE', 'PI'),	('PI', 'TO'), ('PR', 'SC'), ('PR', 'SP'), ('RJ', 'SP'),
		('RS', 'SC')
	]
	g = nx.Graph()
	origin = ''
	destiny = ''

	# -------------------- GRAPH GENERATION --------------------#
	g.add_edges_from(edges)

	# -------------------- DATA INPUT -------------------- #
	o = input('Input the origin: ')
	d = input('Input the destiny: ')

	# Find origin and destiny nodes
	for node in g.nodes():
		if node == o.upper():
			origin = node
		if node == d.upper():
			destiny = node

	# -------------------- SMALLER PATH SEARCH -------------------- #
	print('# %s SEARCHING THE SMALLEST PATH %s #' % ('-' * 20, '-' * 20))
	# If origin or destiny not found, they will have ''
	if origin != '' and destiny != '':
		print('Origin: %s  |  Destiny: %s' % (origin, destiny))
		option1 = search(g, origin, destiny)
		option2 = search(g, destiny, origin)
		if option1[0] < option2[0]:
			result = option1
		else:
			cam = option2[1].split(' ---- ')
			i = len(cam) - 1
			string = ''
			while i > 0:
				string += '%s ---- ' % cam[i]
				i -= 1
			string += '%s' % cam[0]
			option2[1] = string
			result = option2
		print('Jumps: %d\nPath: %s' % (result[0], result[1]))

		generateGraph(g, origin, destiny, result[1].split(' ---- '))
	else:
		print('Ooops! Origin and/or destiny not found.')


if __name__ == '__main__':
	main()
