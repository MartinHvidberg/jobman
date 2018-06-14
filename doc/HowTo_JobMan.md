

# How to - JobMan

These instructions refer to **JobMan version 1.x**

Specifically it's tested against
- __version__ = "1.1.3"
- __build__ = "2018-01-08 - RHEL"

## What JobMan is - and isn't

JobMan is short for 'Job Manager'. This means that JobMan can Manage the execution of thusands, or millions, of jobs. Jobman will ensure that a maximum of jobs is run, in parallel, at any time.

JobMan will not make the jobs, i.e. the task of slicing your huge overall job into smaller bites is not something JobMan will do for you.


## So. What's a Job?

 A job is for for most practical purposes a small script file (on Unix/Linux a shell script, on windows a .bat file).
 If you have to do the same operation for a large number of input items, e.g. have to read through a lot of web pages and store an extract of their contents.


 ### Example: Web page scraping

 You have a long list of web pages that you would like to process. The process, for each web page,  includes:

 1. Downloading all images on the page.
 2. Analyzing all the images.
 3. reporting the result to your company database.


 The analyzing part takes rather longer than the reading and writing data, but you have some strong computers optimized for this - in fact you have three such computers available.

 You now write a small script to process one web page. It might look something like this (in pseudo code).

>download_website_images  www.myfirstsite.net

>analyse_images  --jpg --gif --png  > result_file.dat

>upload_to_DB  --user=jobman  --pass=secret  result_file.dat

Now assume you want to do this for 100.000 web pages, and you have a list of the relevant web addresses. Then you have to create 100.000 small files, identical to the one above, except the web address (www.myfirstsite.net) will be replaced with the addresses from the list.

You will not do this manually, you will write a small script to do it, or otherwise generate the many small job files automatically.

#### All in serial approach
Now you could write a script, simply listing calls to all the other scripts, and run it. Then the web pages would be processed (one at the time) and the job would be done. But lets assume the analysis of each image takes a couple of seconds, with just 10 images per page, that would take a total of 100.000 x 10 x 2 = 2 millions seconds, which is more than 3 weeks ... Too slow.

#### All in parallel approach
Maybee you can write a script file that starts all the jobs, i.e. starting the next job right away, not waiting for the prior jobs to finish. On Unix that can be done with a simple & at the end of each line. This will cause your computer to start processing all 100.000 web pages in parallel. If you have 100.000 CPUs this might be a good idea, but more likely you haven't and then this approach will be hugely inefficient.

#### GNU Parallel, Xargs, subshells, etc.

There exist, in particular on Unix/Linux, a number of way to execute jobs in parallel. And at least some of them would be able to do a really good job here. But remember, we have 3 computers available, all optimized to perform this task. Having several computers collaborating is not trivial, if at all possible, with the classic parallel frameworks.

#### The JobMan approach

JobMan assumes that all the jobs (the 100.000 files in our case) is located in a directory on a shared network - called 'the Master'. Each computer use a local working directory, and must have read+write access to both the local directory and the Master. The Master is subdivided into separate zones for new-jobs, processed-jobs and failed-jobs. JobMan will pick jobs out of the Master, process them locally, and return them to the Master. You can start JobMan on as many computers you want. A local jobman.config file dictates how many jobs to run in parallel, so this can be adjusted individually for each computer.


## How to run Jobman

You need a few things to get started
* A number of *job-files*
* A *directory* to hold the job-files. This place is referred to as 'Master'
* Another *local work-directory*, referred to as 'Worker'
* The contents of the [JobMan](https://github.com/MartinHvidberg/jobman.git) repository (strictly, you only need the */src/jobman.py* file)
* *Python* 2.x (testet on 2.7.5 on RedHat and 2.7.? on win)

For a description of job-files, see the chapter: Example, above.

The two directories may be on the same or separate computers. I case you use several computers for processing, each computer must have a private work-dir, and all computers must be able to access the shared Master.

### 1. Create the Master

Though not absolutely necessary, it's by far the easiest to create the Master first.

Master is (in version 1.x of JobMan) a directory with a number of mandatory sub-directories, and a few files:

* Available/
* Busy/
* Completed/
* Discarded/
* Executables/
* jobman.sh (.bat on windows)
* jobman.config
* (jobman.py)


#### Available/
Is the queue. This is where you put the jobs you want JobMan to manage.

#### Busy/
While a job is in process on a Worker computer, the Master copy of the job file resides in this directory.

#### Completed/
When JobMan successfully finishes with a job, it will return the job-file and the local working directory here. Therefore Completed gets two new object (a file and a sub-directory) for each successfully completed job.

#### Discarded/
Same as Completed, except this is where the job goes if it didn't complete successfully.

#### Executables/
No job files go her. This is where the 'helper' programs are stored. If the job-file is a completely self-contained program, this directory will be empty. But if a helper program or any other shared resource is needed for the execution of a job, the master copy is located here.

#### jobman.sh (.bat on windows)
This file starts a JobMan session, i.e. this is the file you want to run to run JobMan. The insides are described below, in the chapter about the Worker.

#### jobman.config
A master copy of the configuration file. This file **always** need to be edited to match the individual worker, before you run JobMan. The insides are described below, in the chapter about the Worker.

#### jobman.py
Normally the JobMan program file will live here, but jobman.sh (.bat) have an option to get it elsewhere.

### 2. Create the Worker

#### The short version
* Make a local directory
* Copy jobman.sh (.bat) and jobman.config from master
* Edit jobman.sh (.bat) and jobman.config to fit your computer

#### The slightly longer version
Make a local directory. Make sure that the user supposed to run JobMan have full reading and writing access to this directory.

Copy jobman.sh (.bat) and jobman.config from Master to your new local working directory.

Edit jobman.sh (.bat) and jobman.config to fit your computer.

   * jobman.sh (.bat): You will need to correct the location of /Master/Executables/ as well as the path to your local copy of the Python interpreter. If jobman.py is not present, you need to to adjust the optional copying of it from a relevant location. It can be copied from /Master/ or from a git repository of your choice.
   * jobman.config: Contains a number of parameters, that identifies and control the running of JobMan on the specific computer. This inclused the name og the computer, the desired number of parallel processes and the location of the Master and Worker directories. There are comments inside the file to guide you towards meaningful values.

### 3. Run
Run jobman.sh. This will automatically create the two sub-directories you need: workers/ and Executables/ and populate Executables/ with a copy of whats in the Master/Executable. From here JobMan will manage everything for you. If you need to inter-ween you can do so via the jobman.config file. This will allow you to adjust the number of running processes, or pause the queue. When the processing is completed you will se the message: **JobMan complete...**
