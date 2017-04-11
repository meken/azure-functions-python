At the time of this writing Python has experimental support
on Azure Functions. Although it's possible to get things
working, the required information is scattered over 
multiple places. The goal of this repository is to provide
a fully automated example that works end-to-end.

If you click on the deploy button below, an ARM template
will be triggered and the following resources are going
to be provisioned
* An Azure Functions instance and its dependencies 
(Storage, Application Service Plan etc.)
* A DocumentDB instance

In addition this Github repository will be linked to Azure
Functions, the repository will be cloned and the required 
Python packages will be installed in a fully automatic
fashion.

[![Deploy to Azure](http://azuredeploy.net/deploybutton.png)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmeken%2Fazure-functions-python%2Fmaster%2Fazuredeploy.json)
[![Visualize](http://armviz.io/visualizebutton.png)](http://armviz.io/#/?load=https%3A%2F%2Fraw.githubusercontent.com%2Fmeken%2Fazure-functions-python%2Fmaster%2Fazuredeploy.json)

#### Installing packages

Because Python support is experimental, the installation
of additional (pip) packages needed by Azure Functions 
requires some effort. There are two approaches, 
* Creating a Python virtual environment and installing
the packages in there
  * Since the Python handler doesn't take into account 
  the activated environment, you need to add the packages
  directory from virtual environment into the path 
  whenever the installed packages are needed. In this
  example we assume that the virtual environment _env_ is 
  configured at the level of _host.json_ (top level). The 
  following needs to be done before importing the packages
  ```python
  import os, sys

  sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), "..", "env/Lib/site-packages")))
  ```
* Installing a site extension with an alternative Python
 version and configuring the handler mapping to use that 
 installation by default. This will also put the 
 alternative Python in a directory where the current user
 will have write permissions, so pip install will work
 as expected. 

In this example we've opted for the second option as
inspired by https://github.com/Azure/azure-webjobs-sdk-script/issues/519
 
#### Automation

It's possible to log on to the host machine after 
provisioning of the resources and then install the pip packages
through the Kudu command line. However, that would be a manual operation
and hence error prone. Instead, in this repository we're
using the auto configuration mechanism provided by Kudu.
By providing a .deployment file it's possible to alter
the post installation process. In this case a batch file
that runs pip install with the provided requirements.txt
file, is executed after the deployment step, as documented
here: https://github.com/projectkudu/kudu/wiki/Post-Deployment-Action-Hooks

 
