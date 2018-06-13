
# The jobman.config file used to control JobMan

All control of a running JobMan session is done by editing the jobman.config file.
which the running session will read from time to time, and act accordingly.

Note: In general everything is case sensitive.
Note: True | False. Anything != 'True' is considered false, and it may be case sensitive, so 'true' might be interpreted as 'False'.


## Name
Your name, to be used in logs, reports and error messages.
Should not be empty, nor too long as it my be repeated many times in the log files.

Default: Dave

## Computer
The computers name/number, to be used in logs, reports and error messages.
Should not be empty, nor too long as it my be repeated many times in the log files.

Default: GE400
Note: The Default value will likely make JobMan ask you to put in some valid values in your .config file - You shoul'd not be using a 'General Electric 400-series computer'.

## max_threads
Max number of parallel processes. Should be <= the number of CPU cores available.

Default: a number close to the number of CPUs your computer have

## hammertime
Number of seconds between JobMan check if number of running processes is equal to max_threads.

Default: ca. (average job run_time) / (max_threads)

## pilotsaygo
During runtime, set this to False to stop JobMan in a smooth way
When False, JobMan will finish ongoing jobs, but not start new jobs.
If you want to stop your computer, and there are still many jobs in the pool.
Turn this to True, and wait for presently running jobs to complete.

Default = True

## python
The location of the Python interpreter, e.g. C:\python27\python.exe

## Myworkdir
An empty, preferably local, directory, where current user have read and write access.

## jmjqmdir
The directory that contains the JobMan job-queue structure. Current user need to have read and write access here.
