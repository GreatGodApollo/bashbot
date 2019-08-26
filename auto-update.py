# This auto-update script is designed specifically for my environment.
# You will likely need to make modifications for this to work.

# Imports
import sh
from config import Config
from sh import git
import time

# Declarations
serviceName = Config.serviceName
workingDirectory = Config.workingDirectory
service = sh.sudo.service


def CheckForUpdate(workingDir):
    print("Fetching most recent code from source...")

    # Fetch most up to date version of code.
    p = git(f"--git-dir={workingDir}.git/", f"--work-tree={workingDir}", "fetch", "origin", "master")

    print("Fetch Complete.")
    time.sleep(2)
    print(f"Checking status for {workingDir}...")

    statusCheck = git(f"--git-dir={workingDir}.git/", f"--work-tree={workingDir}", "status")

    if "Your branch is up-to-date" in statusCheck:
        print("Status check passes.")
        print("Code up to date.")
        return False
    else:
        print("Code update available.")
        return True


if __name__ == "__main__":

    print("****** Checking for Code Update ******")

    if CheckForUpdate(workingDirectory):
        service(f"{serviceName}", "stop")
        print("Resetting local modifications...")
        resetCheck = git(f"--git-dir={workingDirectory}.git/", f"--work-tree={workingDirectory}", "reset", "--hard",
                         "origin/master")
        print(str(resetCheck))
        service(f"{serviceName}", "start")

