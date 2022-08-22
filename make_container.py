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

    parser.add_argument("--set",
                        metavar="KEY=VALUE",
                        nargs='+',
                        help="Set environment variables for the docker "
                            "container using format key=value(do not put "
                            "spaces before or after the = sign). "
                            "If a value contains spaces, you should define "
                            "it with double quotes: "
                            "foo=\"this is a sentence\". Note that "
                            "values are always treated as strings.")

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
            "--memory", "1024mb",
            "--shm-size", "2g",
            *list(itertools.chain(*list(map(lambda x: ("--env", x), args.set)))),
            "--restart", "always",
            "-d", "{}:{}".format(name, tag)],
        check=True
    )