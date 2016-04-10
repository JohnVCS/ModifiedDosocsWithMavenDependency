#!/usr/bin/python

# Copyright (C) 2016 Jesse Moseman, and John Carlo B. Viernes IV
#
# This file is part of fossologyFunTime.
#
# fossologyFunTime is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# fossologyFunTime is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fossologyFunTime.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-2.0+

import subprocess
import os

 
devnull=open('/dev/null','w')

# creates the temporary directory to store the jar files
def createTempDirectoryIfDoesntExist():
	newpath = r'mydep' 
	if not os.path.exists(newpath):
    		os.makedirs(newpath)

# copies depedencies to folder 
def copyDependencyToTempFolder():
	copyDepCmd=["mvn","dependency:copy-dependencies","-DoutputDirectory=mydep","-Dclassifier=sources"]
	copyDepMvnPluginProcess=subprocess.call(copyDepCmd, stdout=devnull)

# creates the graphML
# graphML is one of the supported output type format of Maven
def createGraphMl():
	createGraphMlCommand = ["mvn", "dependency:tree","-DoutputFile=test.graphml", "-DoutputType=graphml"]
	#.call(...) is for blocking
	createGraphMlMvnPluginProcess = subprocess.call(createGraphMlCommand, stdout=devnull)

# parses graphml file and returns dependency tuples
# basically it shows the parent-child relationship in a sort of like a pair
def parseGraphMl():
	import networkx
	import os.path
	import time
	
	# graph is an oject imported by networkx
	graph=networkx.read_graphml("test.graphml")
	
	# optional argument data="NodeLabel" since that is what we need
	# nodes grabs all the nodes and nodelabel, and then returns a set of tuples
	# dict changes the comma to colon so we can grab the id's and labels
	# essentially, the purpose is to map the node-id to package name 
	nodesDict=dict(graph.nodes(data="NodeLabel"))
	# print(dict(graph.nodes(data="NodeLabel")))
	edgeLabels=[]
	for e1,e2 in graph.edges():
		edgeLabels.append((nodesDict[e1]['label'],nodesDict[e2]['label']))
	return edgeLabels

def createDocumentForArtifact(artifact):
	dosocsOneshotCommand = ["dosocs2", "oneshot",artifact]
	#.call(...) is for blocking
	dosocsOneshotProcess = subprocess.call(dosocsOneshotCommand)#, stdout=devnull)

def createDocumentsForDepedencies():
	for filename in os.listdir('mydep'):
		dosocsOneshotCommand = ["dosocs2", "oneshot","mydep/"+filename]
		#.call(...) is for blocking
		dosocsOneshotProcess = subprocess.call(dosocsOneshotCommand)#, stdout=devnull)


def getDepAndGenDocsForDeps():
	createTempDirectoryIfDoesntExist()
	copyDependencyToTempFolder()
	createDocumentsForDepedencies()


# main method
if __name__ == '__main__':
	# get dependencies and generate documents
	# getDepAndGenDocsForDeps()

	#createGraphMl()
	edgeLabels=parseGraphMl()
	for e in edgeLabels:
		print e
