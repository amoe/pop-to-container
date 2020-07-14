# pop-to-container

A simple SSH tunnel script to ease connecting to containers in UoS
infrastructure.

## Install prerequisites

Please use Fabric v2.4.0.  To install, do: `pip3 install fabric==2.4.0`

## How to use

python3 pop-to-container.py PROFILE

Where PROFILE is `factchecking`, or `brat`.

## Windows

It's not working on windows at the moment.  I think there's some kind of issue
with the tunnel setup.  This could possibly be addressed by using the
`sshtunnel` pypi package instead of fabric.
