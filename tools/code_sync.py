import click
import os
import subprocess


@click.command()
@click.argument("repo_path")
@click.argument("host")
@click.option("--include-git", is_flag=True, help="Include the .git directory.")
@click.option(
    "--dest",
    default=None,
    help="Specify a specific destination path on the remote host.",
)
def code_sync(repo_path, host, include_git, dest):
    """
    Sync code to a remote host using rsync.

    Args:
        repo_path (str): The local repository path to sync.
        host (str): The remote host to sync the code to.
        include_git (bool): Flag to include the .git directory in the sync.
        dest (str, optional): Specific destination path on the remote host. Defaults to None.

    Returns:
        None

    Raises:
        SystemExit: If the local path does not exist or is not a directory.
        SystemExit: If the local path is outside the home directory and --dest is not specified.

    This function uses the rsync command to synchronize the local repository to a remote host.
    It constructs the rsync command based on the provided arguments and executes it.
    If the local path is within the user's home directory, it calculates the relative path
    and uses it as the remote path. Otherwise, it requires the --dest option to be specified.
    The function also handles excluding files or directories specified in a .syncignore file
    located in the sync directory.
    """

    local_path = os.path.abspath(os.path.expanduser(repo_path))
    if not os.path.isdir(local_path):
        click.echo(
            f'Error: Local path "{local_path}" does not exist or is not a directory.'
        )
        return

    # Determine the remote path
    home_dir = os.path.expanduser("~")
    if dest:
        remote_path = dest
    else:
        if local_path.startswith(home_dir):
            rel_path = os.path.relpath(local_path, home_dir)
            remote_path = f"~/{rel_path}"
        else:
            click.echo(
                "Error: Local path is outside the home directory. Please specify --dest."
            )
            return

    # Create the remote directory if it doesn't exist
    ssh_command = f'ssh {host} "mkdir -p {remote_path}"'
    click.echo("Running command: " + ssh_command)
    result = subprocess.run(ssh_command, shell=True)
    if result.returncode != 0:
        click.echo("Error: Failed to create remote directory")
        return

    # Build the rsync command
    rsync_command = ["rsync", "-avz", "--delete"]

    # Check for .syncignore file
    syncignore_path = os.path.join(local_path, ".syncignore")
    if os.path.isfile(syncignore_path):
        rsync_command += ["--exclude-from", syncignore_path]
    else:
        # Exclude .git if include_git is not set
        if not include_git:
            rsync_command += ["--exclude", ".git"]

    rsync_command += [local_path + "/", f"{host}:{remote_path}"]

    # Execute the rsync command
    click.echo("Running command: " + " ".join(rsync_command))
    result = subprocess.run(rsync_command)
    if result.returncode != 0:
        click.echo("Error: rsync failed")


if __name__ == "__main__":
    code_sync()
