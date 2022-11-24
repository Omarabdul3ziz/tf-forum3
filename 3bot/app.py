from uuid import uuid4
import base64
import json

from nacl.public import Box
import nacl.encoding
import nacl.signing
import requests

from flask import Flask, session, redirect, url_for, request, abort, jsonify
from flask_sessionstore import Session
import os

from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import Base64Encoder

app = Flask(__name__)
app.config['private_key'] = "FXYLXCFp3WnEEb2c+SPEJUhYdVQpPuN2fAgWzApWQns="
SECRET_KEY = "flasksecret"
SESSION_TYPE = 'filesystem'
SESSION_PERMANENT = True
app.config.from_object(__name__)
Session(app)


@app.route('/pub_key')
def get_public_key():
    state = str(uuid4()).replace('-', '')
    session['state'] = state
    print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("entered the /pub_key")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    # private_key = nacl.signing.SigningKey(app.config['private_key'], encoder=nacl.encoding.Base64Encoder)
    # public_key = private_key.verify_key
    # return jsonify(
    #   {'state': state, 'pk': public_key.to_curve25519_public_key().encode(encoder=nacl.encoding.Base64Encoder).decode()})
    sign_key = SigningKey(
        app.config['private_key'], encoder=nacl.encoding.Base64Encoder)
    print("\n sign", sign_key, "\n")
    verification_key = sign_key.verify_key
    print("\n verify", verification_key, "\n")

    vk_bytes = verification_key.to_curve25519_public_key().encode(
        encoder=Base64Encoder).decode()
    print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(state)
    print(vk_bytes)
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

    return jsonify({'state': state, 'pk': vk_bytes})


@app.route('/data')
def data():
    print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("entered the /data")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    data = request.args.get('signedAttempt')

    if not data:
        return abort(400, jsonify({'message': 'Bad request, some params are missing'}))

    data = json.loads(data)

    username = data['doubleName']
    if not username:
        return abort(400, jsonify({'message': 'Bad request, some params are missing'}))

    res = requests.get("https://login.threefold.me" + '/api/users/{0}'.format(username),
                       {'Content-Type': 'application/json'})
    if res.status_code != 200:
        return abort(400, jsonify({'message': 'Error getting user pub key'}))

    # should the pub-key be the same as the generated from the /login func above?
    user_pub_key = nacl.signing.VerifyKey(
        res.json()['publicKey'], encoder=Base64Encoder)

    # verify data
    signedData = data['signedAttempt']
    if not signedData:
        return abort(400, jsonify({'message': 'Bad request, some params are missing'}))

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>.")
    print(signedData)
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

    verifiedData = user_pub_key.verify(base64.b64decode(signedData)).decode()

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>.")
    print(verifiedData)
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    data = json.loads(verifiedData)

    if not data:
        return abort(400, jsonify({'message': 'Bad request, some params are missing'}))

    if data['doubleName'] != username:
        return abort(400, jsonify({'message': 'Bad request'}))

    # verify state
    state = data['signedState']

    if not state:
        return abort(400, jsonify({'message': 'Bad request'}))

    nonce = base64.b64decode(data['data']['nonce'])

    ciphertext = base64.b64decode(data['data']['ciphertext'])

    private_key = SigningKey(
        app.config['private_key'], encoder=nacl.encoding.Base64Encoder)

    box = Box(
        private_key.to_curve25519_private_key(),
        user_pub_key.to_curve25519_public_key()
    )

    # try:

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>.")
    print("enter try block")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

    decrypted = box.decrypt(ciphertext, nonce)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>.")
    print("the decrypted")
    print(decrypted)
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

    result = json.loads(decrypted)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>.")
    print("the resutl")
    print(result)
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    email = result['email']['email']
    sei = result['email']['sei']
    res = requests.post("https://openkyc.live/verification/verify-sei", headers={'Content-Type': 'application/json'},
                        json={'signedEmailIdentifier': sei})
    if res.status_code != 200:
        return abort(400, jsonify({'message': 'Email not verified!'}))
    result['email']['username'] = username
    return jsonify(result['email'])
    # except:
    #   return abort(400, jsonify({'message': 'Error decrypting'}))


if __name__ == "__main__":
    app.run()
