<a href="https://forums.threefold.io/"><img src=
"https://forums.threefold.io/images/discourse-logo-sketch.png"

ThreeFold forums is the 100% open source discussion platform built for the next decade of the Internet. [forked from **discourse.org**](https://www.discourse.org) Use it as a:

- mailing list
- discussion forum
- long-form chat room

To learn more about the philosophy and goals of the project, [visit **forums.threefold.io**](https://forums.threefold.io/).
# Install

- Dev:  cd {src_code}` then `d/boot_dev --init`
- database files are in directory `{src_code}/data` if you want to delete db totally and reiitialize, delete this directory and `docker rm -f discourse_dev`
- 3bot service runs in tmux in user : `discourse`

# RUn
- Dev: `./bin/docker/unicorn`