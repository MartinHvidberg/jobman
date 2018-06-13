

# How to - JobMan


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
Maybee you can write a script file that starts all the jobs, i.e. starting the next job right away, not waiting for the prior jobs to finish first. On Unix that can be done with a simple & at the end of each line. This will cause your computer to start processing all 100.000 web sites in parallel. If you have 100.000 CPUs this might be a good idea, but more likely you haven't and then this approach will be hugely inefficient.

#### GNU Parallel, Xargs, subshells, etc.

There exist, in particular on Unix/Linux, a number of way to execute jobs in parallel. And at least some of them would be able to do a really good job here. But remember, we have 3 computers available, all optimized to perform this task. Having several computers collaborating is not trivial, if at all possible with the classic parallel frameworks.

#### The JobMan approach

JobMan assumes that all the jobs (the 100.000 files in our case) is located in a directory on a shared network - called 'the pool'. Each computer use a local working directory, and must have read+write access to both the local directory and the pool. The pool is subdivided into separate zones for Non-processed jobs, processed jobs and failed jobs. JobMan will pick jobs out of the pool, process them locally, and return them to the pool. You can start JobMan on as many computers you want. A local jobman.config file dictates how many jobs to run in parallel, so this can be adjusted individually for each computer.
