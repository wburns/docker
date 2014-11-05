#!/usr/bin/env python
#
############################################################################
#
# Name: handle_pull_request
# Author: Manik Surtani (http://github.com/maniksurtani)
# Description: This script handles pull requests on a topic branch from a 
#              specified remote repository, merges it to a specified branch, 
#              and optionally pushes the updated branch to the local repo's origin.  
#
# Configuration: The following variables need to be set.

ORIGIN_REPO="origin" # The fork of upstream.  Can be a named remote or a full URL.
GIT="git" # Path to the git binary executable
TMP_BRANCH="___tmp___"
#
############################################################################

import sys
import subprocess

class Colors(object):
  MAGENTA = '\033[95m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  CYAN = '\033[96m'  
  END = '\033[0m'
  UNDERLINE = '\033[4m'  
  
def helpAndExit():
  print '''
  Usage: handle_pull_request <remote repo to pull from> <branch on remote repo> <local release branch to merge into> [-p]
  
        The -p flag issues a push to the origin after pulling in changes from a forked repository.  Useful if you know the 
        changes are small and can be safely pushed.  If -p is not specified you would need to run a push manually.
  '''
  sys.exit(1)

def run_git(opts):
  call = [GIT]
  for o in opts.split(' '):
    if o != '':
      call.append(o)

  print "Calling git via %s!" % call
  return subprocess.Popen(call, stdout=subprocess.PIPE).communicate()[0]

def is_not_empty(n):
  return n != ''

def colorize(txt, color):
  return "%s%s%s" % (color, txt, Colors.END)

def commit_msg(commit):
  return run_git('show --pretty=format:"%%s" %s' % commit).split('\n')[0]

def main():
  if len(sys.argv) < 4:
    helpAndExit()
  
  remote = sys.argv[1]
  remote_branch = sys.argv[2]
  release_branch = sys.argv[3]
  
  push = False
  if len(sys.argv) > 4:
    if sys.argv[4] == "-p":
      push = True
  
  print "Merging changes from repo %s (branch %s) and merging into %s" % (colorize(remote, Colors.MAGENTA), colorize(remote_branch, Colors.MAGENTA), colorize(release_branch, Colors.MAGENTA))
  
  try:    
    ## Create a new temp branch to work on, based off 'release_branch'
    run_git("checkout -q -b %s %s" % (TMP_BRANCH, release_branch))
    
    ## Pull changes from the remote branch on the remote repo, onto the temp branch
    run_git("pull -q %s %s" % (remote, remote_branch))
    
    ## List the commits here - IN REVERSE ORDER!
    response = run_git('--no-pager log --pretty=format:%%h --no-merges --reverse %s..HEAD' % release_branch)
    commits = filter(is_not_empty, response.split("\n"))
    
    ## Switch to the release branch again
    run_git("checkout -q %s" % release_branch)
    
    ## And cherry-pick the commits, one at a time, oldest first (hence the reverse order above)
    if len(commits) == 0:
      print "%s: No commits found!! Aborting!!" % colorize("WARNING", Colors.RED)
      sys.exit(1)

    for commit in commits:
        run_git("cherry-pick %s" % commit)
    
    ## Push to origin if we are configured to do so    
    if push:
      run_git("push %s %s" % (ORIGIN_REPO, release_branch))
      print "Branch %s on remote %s merged into %s and pushed to upstream." % (colorize(remote_branch, Colors.GREEN), colorize(remote, Colors.GREEN), colorize(release_branch, Colors.GREEN))
    else:      
      print '''
Branch %s on remote %s merged into %s.
 
** %s: Nothing has been pushed yet; please inspect the commit log and run

    %s git push origin %s %s

%s if you are happy with the commits.''' % (remote_branch, remote, release_branch, colorize('NOTE', Colors.RED), Colors.CYAN, release_branch, Colors.END, colorize('only', Colors.UNDERLINE))
    
  finally:  
    ## Cleanup
    run_git("checkout -q %s" % release_branch)
    run_git("branch -D %s" % TMP_BRANCH)

if __name__ == "__main__":
  main()
