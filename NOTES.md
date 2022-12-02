<a href="https://forums.threefold.io/"><img src=
"https://forums.threefold.io/images/discourse-logo-sketch.png"></a>

ThreeFold forums can be used as a:

- mailing list
- discussion forum
- long-form chat room

To learn more about the philosophy and goals of the project, [visit **forums.threefold.io**](https://forums.threefold.io/).

Chnages on the fork:

- update the identity (images/logos) to ThreeFold.
- add Threefold auth.

### Threebot implementation

- Using [PyNaCl](https://pynacl.readthedocs.io/en/latest/) for Signing/Verifing and Encryption.
- the Oauth proxy is built in python find it in `3bot/` exposes two endpoints `pub_key` and `data`
- the app server (ruby) will have to extra endpoints `/threebot/login` and `/threebot/callback` calling methods defined in `app/controllers/threebot_controllers.rb`
- the default login/signup in the UI should be disabled and instead will add a button to call the `/threebot/login` endpoint.

- The flow:

  - button from the UI is clicked calling the `/threebot/login` endpoint.
  - `/threebot/login` gets the public key from the Oauth server `/pub_key` and redirects the user to 3bot connect url
  - in the `/pub_key` a base64 signing key is imported *create at oauth server start*, and responed with a public key drived from the signing key with a state
  - `/threebot/callback` the callback endpoint that receives the data from 3bot connect and sends it to Oauth server to verify
  - where `/data` gets the public key for the user and verify the signedData decrypt the ciphertext and send it back to the ruby app
  - a session is added for the loggedin/signedup user.

- for further clarification on this point check the [Oauth Proxy](https://github.com/threefoldtech/oauth-proxy)

### Run for Development

- For running discourse check the [Fresh Ubuntu Install Guide](https://github.com/discourse/discourse/blob/main/docs/DEVELOPER-ADVANCED.md)
- For running the oauth server

  ```bash
  apt update
  apt -y install python3-pip libglib2.0-dev libcairo2 libcairo2-dev python3-apt libgirepository1.0-dev
  cd /3bot
  pip3 install -r requirements.pip

  uwsgi --socket 0.0.0.0:5000 --protocol=http -w app:app
  ```
- if you running the app on remote serever you will need to run a proxy to accept requests from the bind address
`bin/ember-cli`, now you can access the app on `ip:4200`
- Since this is not the supported way to run discourse you will face an issue after redirected back from threebot site to the app. you will need to

    - use http instead of https
    - update the ip *if you accessing a remote server. you will not need this step if you run it locally*
