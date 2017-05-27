# Basic idea in jobman 

Jobman enables a computer to ask for a package of work, execute it, and return the result...

The overall idea is to utilise some of the idle time on our office computers, in particular at night and during the weekend, to help us with some calculations that would otherwise take weeks on a single computer.

The concept is based on the idea of a pool of small(er) work packages. I'll get back to details on the packages in a moment. 

## Implimentation via shared disk/directory

This is the working mode of ver. 1.x. 

### The shared pool of work


### The local 'worker' computer 

## Implimetation via Message Que

This is the working mode of a feature implimentation, lakely ver. 2.0, or something like that...

### Pool

The pool is, in the present implementation a Message Queue server (specifically a RabbitMQ server) with a public hiring queue where 'employers' can announce that they have work to offer. They do not queue the actual work packages on this public queue, just a message that they need workers. This message is persistent and can be read from the queue many times, by many workers. It should be removed, by it's original poster, when all the work is completed.

The worker can read from the public hiring queue to find employment. The worker replies to the employer, via the employers 'ask for work' queue, to ask for actual work packages.

The further exchange of work and replies, is send via private queues (one in each direction) between the worker and the employer.

### Step-by-step

Please refer to illustration: jobman_ill_1 for the following, more stepwise, explanation.

There exist one public and permanent queues on the server, for announcing that work are available. The queues name is _jobman_.

1. An employer 'E' have work to share. He puts a persistent message in the public hiring queue _jobman_, to announce that work is available. This message contains the name, and other relevant details, for E's 'ask for work' queue.

2. A worker 'W' scans the public hiring queue and sees the message. 

3. 'W' then post a message back to E's 'ask for work' queue, that he is free to receive work. At the same time 'W' opens two new queues on the server, and he sends the relevant queue-names and other details, in the message to 'E', so the two new queues can be considered private between the two. One of the new queues are from 'E' to 'W' for sending work packages, and the other queue is from 'W' to 'E' for returning the work results.

4. 'E' notice the message on his 'ask for work' queue.

5. 'E' send a work package to 'W', via their private work queue. This first work package would normally be a ability-test with a small test-work-set. It serves the purpose of checking that 'W' can in fact execute the relevant type of software, and produce the desired result.

6. 'W' receives the work package, and executes the work

7. 'W' returns the result of the work to the private reply queue.

8. 'E' receives the results, and evaluates them.

If 'E' finds the result to be satisfying, then 5,6,7,8 can repeat, for as long as 'E' has work and 'W' is willing to accept more work.



###The Packages

