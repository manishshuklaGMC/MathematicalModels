import numpy as np 
import networkx as nx
import gossip as gs
import random
import matplotlib.pyplot as plt
from operator import itemgetter
import community

class network:
	def __init__(self, n, m, p):
#		self.network = nx.DiGraph()
		self.network = nx.powerlaw_cluster_graph(n, m, p, seed=None) 
		self.newman_watts = nx.newman_watts_strogatz_graph(n, m, p, seed=None)
		self.watts = nx.watts_strogatz_graph(n, m, p, seed=None)
		self.barabasi = nx.barabasi_albert_graph(n, m, seed=None)
#		self.ergodic = nx.erdos_renyi_graph(n, p, seed=None)
		nx.write_gml(self.watts,"watts.gml")
#		nx.write_gml(self.ergodic,"ergodic.gml")
		nx.write_gml(self.newman_watts,"newmanWatts.gml")
		nx.write_gml(self.network,"powerLaw.gml")
		nx.write_gml(self.barabasi,"barabasi.gml")	

	def assign_information_value(self, sigma): 				#calculating mew for every vertex based on homophily
		for n,d in self.network.nodes_iter(data=True):
			self.network.node[n]['mew'] = []
			self.network.node[n]['color'] = 0
			self.network.node[n]['mewFinal'] = 0
		for n,d in self.network.nodes_iter(data=True):
			if len(self.network.node[n]['mew']) == 0:
				self.network.node[n]['mew'].append(random.random())
				for j in self.network.neighbors(n):
					random_number = random.gauss(np.mean(self.network.node[n]['mew']), sigma)
					while (random_number<0 or random_number>1.0):
						random_number = random.gauss(np.mean(self.network.node[n]['mew']), sigma)
					self.network.node[j]['mew'].append(random.gauss(np.mean(self.network.node[n]['mew']), sigma))
			else:
				for j in self.network.neighbors(n):
					random_number = random.gauss(np.mean(self.network.node[n]['mew']), sigma)
					while (random_number<0 or random_number>1.0):
						random_number = random.gauss(np.mean(self.network.node[n]['mew']), sigma)
					self.network.node[j]['mew'].append(random_number)
		for n,d in self.network.nodes_iter(data=True):
			if len(self.network.node[n]['mew'])>0:
				self.network.node[n]['mewFinal'] = np.mean(self.network.node[n]['mew'])
			else:
				self.network.node[n]['mewFinal']=0
#			print self.network.node[n]['mew_final']

	def gossip_value_for_edge(self):
		max_degree = 0
		for n,d in self.network.nodes_iter(data=True):
			if max_degree < self.network.degree(n):
				max_degree = self.network.degree(n)

		for m in self.network.edges_iter():
			self.network.edge[m[0]][m[1]]['gossip'] = (self.network.degree(m[0])*self.network.degree(m[1])*1.0)/(max_degree*max_degree)
#			print self.network.edge[m[0]][m[1]]['gossip']

	def information_diffusion(self, num_nodes, beta):
#		patients_zero = [random.randint(0,num_nodes) for r in xrange(beta)]
#		for i in patients_zero:
#			self.network.node[i]['color'] = 1
#		print patients_zero
#		for i in patients_zero:
#			for j in self.network.neighbors(i):
		root_node = random.randint(0,num_nodes-1)
		self.network.node[root_node]['color']=1
		ordered_edges = list(nx.bfs_edges(self.network,root_node))
#		print ordered_edges 
		t_name = "plots/file_name"
		count = 0
		for i in ordered_edges:
			count = count +1 
#			print self.network.node[i[0]]['color']==1,  self.network.node[i[1]]['color']==0
			if(self.network.node[i[0]]['color']==1 and self.network.node[i[1]]['color']==0):
#				probability =100* self.network.node[i[1]]['mew_final']*self.network.edge[i[0]][i[1]]['gossip']
				probability = random.random()
#				print i, probability
				if probability > beta:
#					print "hello from other side"
					self.network.node[i[1]]['color']=1
			if(count%100==0):
				name = t_name + str(count)+".gml"
#				name_other = t_name + str(count)+".gexf"
#				nx.write_gml(self.network,name)
#				nx.draw(self.network)
#				plt.show()
#				nx.write_gexf(self.network,name_other)
		
#		pos=nx.spring_layout(self.network)
#		nx.draw(self.network)
#		plt.show()				
	def degree_frequency(self):
		deg_f = nx.degree_histogram(self.network)
		print deg_f
		deg = nx.degree(self.network)
		list_sorted = sorted(deg.items(),key=itemgetter(1), reverse=True)
#		for i in range(5):
#			print list_sorted[i][0]
#			self.network.remove_node(list_sorted[i][0])
#		nx.write_gml(self.network,"powerLawDeleted.gml")
		for i in list_sorted:
			if i[1]>20:
#				self.network.remove_node(i[0])
				self.network.node[i[0]]['color']=2
			else:
				break
		nx.write_gml(self.network,"powerLawDeleted.gml")
	def cluster_community(self):
		partition = community.best_partition(self.network)
		print partition


num_nodes = 2500
m = 2
p = 0.8
beta = 0.2
sigma = 0.3
x = network(num_nodes,m,p)
x.assign_information_value(sigma) #sigma = standard deviation
x.gossip_value_for_edge()
#x.information_diffusion(num_nodes, beta) #number of patient zeros
x.degree_frequency()
