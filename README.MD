# s-lang

A python library which can be added to a bot implementation to enable the parsing of bot definition files into a traversable action tree based on state.

# Install
The library is hosted on GCP Artifact Repository (for ease of use). To install, first login to GCP and run the following (will change later):
``` 
gcloud auth login
gcloud artifacts print-settings python --project=rare-ethos-384523 --repository=swarmly-python-repo --location=australia-southeast1
```

Apply the output changes to the relevant pip files.

Run:
```pip install s-lang```

# Getting started
Statements are the top level operators for each concept. When building a graph, these will be nodes and the contents of each statement can itself contain statements which evaluate to nodes or operators which are evaluated to adjust the edge or node properties of the statement node. 

Operators parse rules and operate on state to either produce a value which can be resolved contextually by the specific operator or produce a signal which can be used to create a link to another node, for example.

# First Steps
In order to build our decision tree we need to start by computing the beliefs of the current state. Each computed belief should produce a graph in which nodes can be mapped to unique global nodes and then connect to the task and belief graphs.

With those nodes created we can as needed compute the task and belief graphs.


