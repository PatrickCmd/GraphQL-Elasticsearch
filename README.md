# GraphQL and Elasticsearch 
Implementing simple CRUD and Search Operations using GraphQL and Elasticsearch

## Installing Elasticsearch service(MacOS)
```
brew update
brew cast install java
```
### Then install elasticsearch
```
brew install elasticsearch
```
### Starting elasticsearch service
Run the command below in commandline/terminal
```
elasticsearch
```
### Confirming elasticsearch is installed successfully
If you have curl installed, run the command in another terminal tab
```
curl -XGET 'localhost:9200'
```
### Response
You get the response similar to the one below
```
{
  "name" : "jzftZxE",
  "cluster_name" : "elasticsearch_patrick", 
  "cluster_uuid" : "8OmNMgH8Q1myChVMwGchdw",
  "version" : {
    "number" : "5.5.2",
    "build_hash" : "b2f0c09",
    "build_date" : "2018-04-30T12:33:14.154Z",
    "build_snapshot" : false,
    "lucene_version" : "6.6.0"
  }, 
  "tagline" : "You Know, for Search"
}
```
OR paste **http://localhost:9200** and you get the same JSON response

## Install elasticsearch-python client
Make virtual environment
```
virtualenv env
```
Inside the environment in the command line install elasticsearch.
```
pip install elasticsearch
```
