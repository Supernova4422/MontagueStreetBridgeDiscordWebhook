#!/usr/bin/env python
import itertools
import subprocess
import pathlib
import argparse
import random

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run or update a docker container."
    )

    parser.add_argument(
        "--name", metavar='N', type=str, required=True,
        help="An identifier for the container.")

    parser.add_argument(
        "--webhook", metavar='N', type=str, required=True,
        help="Webhook to discord")

    args = parser.parse_args()
    name = args.name
    tag = str(random.randint(0, 99999))
    project_path = pathlib.Path(pathlib.Path(__file__).parent).absolute()

    subprocess.run(
        args=[
            "docker", "build",
            "-t", "{}:{}".format(name, tag),
            "-f", "dockerfile", str(project_path)],
        check=True
    )

    subprocess.run(
        args=["docker", "stop", name],
        check=False
    )

    subprocess.run(
        args=["docker", "rm", name],
        check=False
    )

    out = subprocess.run(
        args=[
            "docker", "images", name,
            "--no-trunc",
            "--filter", "before={}:{}".format(name, tag),
            "--format", "{{.Tag}}"
        ],
        check=False,
        stdout=subprocess.PIPE
    )

    other_tags = out.stdout.decode().splitlines()
    for other_tag in other_tags:
        subprocess.run(
            args=["docker", "rmi", "{}:{}".format(name, other_tag)],
            check=False
        )

    subprocess.run(
        args=[
            "docker", "run", "-dit",
            "--name", "{}".format(name),
            "--env", ("webhook=" + args.webhook),
            "--restart", "always",
            "-d", "{}:{}".format(name, tag)],
        check=True
    )
