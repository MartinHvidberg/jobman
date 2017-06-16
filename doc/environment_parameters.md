
# Environmental parameters used to control JobMan

## Controling JobMan.py

### %dont_start_new_jobs%

True | False (anything != 'True' is considered false)

If you want to stop your computer, and there are still many jobs in the pool.
Turn this on, and wait for presently running jobs to complete.


## Controling the executing jobs (not garatied to always work)


### %jobman_keep_temp_files%

True | False (anything != 'True' is considered false)

If true the executing job should not delete (clean up) its temp files, but rather return them with the result.
The temp files can be valuable in a debugging/testing context.