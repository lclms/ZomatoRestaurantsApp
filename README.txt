
*****************************************************************************************
IMPORTANT
*****************************************************************************************

Before continuing to read this README file, check the labs slides about visualization 
in a web application

*****************************************************************************************
Setting up the application
*****************************************************************************************

1. Create a directory and put there the given application structure. Let us say the base directory of this application is airbnbApp

2. Open a Terminal window and move to the directory ZomatoRestaurantsApp

3. Initialize a virtual environment e.g. named env. Administrator privileges are required
to install virtualenv

$ pip3 install virtualenv
$ virtualenv –p python3 env
$ source env/bin/activate

If you are using Microsoft Windows, the activation command is:

$ env\Scripts\activate

First, a subdirectory env has been created inside airbnbApp and all files associated 
with the virtual environment will be inside it. Then the virtual environment is activated. 

When a virtual environment is activated, the location of its Python interpreter is added to the PATH environment variable in your current command session, which determines where to look for executable files. Notice that the activation command modifies your command prompt to include the name of the environment as:

(env) $

After a virtual environment is activated, typing commands will invoke the interpreter from 
the virtual environment instead of the system-wide interpreter. Having more than one Terminal window implies that we should activate the virtual environment in each of them.

To restore the PATH environment variable for the Terminal session and the command prompt to their original states, we should invoke:

(env) $ deactivate

4. Install the dependencies

If a requirements file exists e.g. requirements.txt we can install all the dependencies it relates to:

$ pip3 install –r requirements.txt

But if not, we have to install one by one, Flask, CherryPy, Paste and Pandas, as follows:

(env) $ pip3 install flask
(env) $ pip3 install cherrypy
(env) $ pip3 install paste
(env) $ pip3 install pandas

You can check what packages are installed in the virtual environment at any time using the pip3 freeze command. Hence we can create the requirements file like:

(env) $ pip3 freeze > requirements.txt

*****************************************************************************************
FAQ
*****************************************************************************************

What problem does a virtual environment solve? 

The more Python projects you have, the more likely it is that you need to work with different versions of Python libraries, or even Python itself. Newer versions of libraries for one project can break compatibility in another project. Virtual environments are independent groups of Python libraries, one for each project. Packages installed for one project will not affect other projects or the operating system’s packages.

Why using a requirements file?

It is a good practice for applications to include a requirements file that records all the package dependencies, with the exact version numbers. This is important in case the virtual environment needs to be regenerated on a different machine, such as the machine on which the application will be deployed for production use. 

*****************************************************************************************
Purpose and working of this web application
*****************************************************************************************

This application is an online data model web service using Spark and Flask

The web service critically depends on 3 Python files:

    1. model.py, that defines the model engine, wrapping inside all the Spark related computations;
    2. app.py, holding a Flask web application that defines a RESTful-like API around the model engine;
    3. server.py, to initialise a CherryPy web-server after creating a Spark session/context and Flask web app.

How it works

When the model engine is initialised, we need to generate our data model based on the data we have in a file. We will do things of that kind in the __init__ method of the ZomatoRestaurantsApark class.

And when using the functionality of filtering data, we need to fetch the correspondent listings/derived information again. But this time around we do not need to read data gain nor to setup the sql table view.

Recall that Flask is a web microframework for Python. It is very easy to start up a web API, by just using some annotations to associate service end-points with Python functions. In our case we will wrap our ZomatoRestaurantsApark methods around some of these end-points and interchange JSON formatted data with the web client.

Basically we use the app as follows:

a) Initialising the application

We init the application when calling create_app. Here the ZomatoRestaurantsApark object is created and then we associate the '@main.route' annotations mentioned above. Each annotation is defined by:
    - A route, that is its URL and may contain parameters between <>. They are mapped to 
        the function arguments;
    - A list of HTTP available methods.

There is an annotation that deserves particular attention
    GET /filtering - to get listings with parameter values by default
    POST /filtering - to get listings with parameter values entered via user interface

b) Deploying a WSGI server using CherryPy

Among other things, the CherryPy framework features a reliable, HTTP/1.1-compliant, WSGI thread-pooled web-server. It is also easy to run multiple HTTP servers (e.g. on multiple ports) at once. All this makes it as a perfect candidate to easily deploy a production web server for our online data model service.

The use that we will make of the CherryPy server is relatively simple. It is a pretty standard use of CherryPy. If we look at the __main__ entry point, we do three things:

    i) Creating a Spark session/context as defined in the function init_spark_session, 
        passing additional Python modules there;
    ii) Creating the Flask app calling the create_app we define in app.py;
    iii) Running the server itself.

c) Running the server with Spark

In order to have the server running while being able to access a Spark context and cluster, we need to submit the server.py file to pyspark, by using spark-submit. We should not use pyspark directly. 

The different parameters when using this command are better explained in the Spark documentation. The --master parameters must point to the Spark cluster setup, which can be local.

In our case, we can use something like this: 

/usr/share/spark/bin/spark-submit --master spark://192.168.1.105:7077 --total-executor-cores 8 --executor-memory 6g server.py 

Or even running with 2 threads in the personal computer:

spark-submit --master local[2] server.py 

We provide a script file containing these commands, called start.sh. It all starts with the following command in a Terminal window:

(env) $ ./start.sh


d) Issue when using multiple scripts and spark-submit

There is one issue we need to work around when using Spark in a deployment like this. A Spark cluster is a distributed environment of workers orchestrated from the Spark Master where the Python script is launched. This means that the master is the only one with access to the submitted script and local additional files. If we want the workers to be able to access additional imported Python modules, they either have to be part of our Python distribution or we need to pass them implicitly. For example, we can do this by adjusting the SPARK_CODE variable to be used when the spark context is created.

e) Using the online web application

Now we just have to open a browser and pointing to

http://0.0.0.0:5678/

or 

http://localhost:5678

Notice that 5678 is the port number set in the application. It could have been other as long as it was fit for the purpose.

BUT when using the iscte.me server, the browser must be pointing to

http://iscte.me/p/5678

(as a note, the p has been added to deal with various users running the server simultaneouly)


