import time
import os, sys
from os import path
import more_itertools
from  more_itertools import unique_everseen
from operator import itemgetter
import psycopg2
import sys
import pprint
import requests
# Contains methods used to build and parse XML
import xml.etree.ElementTree as ET
import urllib
import zipfile
import shutil
import json
import binascii
#
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from base64 import b64decode


import logging
from util.import_config import import_config

# Import settings from config file
tab_server_settings, postgres_settings, download_settings, email_settings, schedule_settings = import_config()

tab_server_url = tab_server_settings['tab_server_url']
tableau_username = tab_server_settings['tableau_username']
tableau_user_pw = tab_server_settings['tableau_user_pw']


session = requests.Session()

def getServerSettingsUnauthenticated():
    payload = "{\"method\":\"getServerSettingsUnauthenticated\",\"params\":{}}"
    endpoint = "getServerSettingsUnauthenticated"
    url = tab_server_url + "/vizportal/api/web/v1/"+endpoint
    print url
    headers = {
        'content-type': "application/json;charset=UTF-8",
        'accept': "application/json, text/plain, */*",
        'cache-control': "no-cache"
        }
    response = session.post(url, data=payload, headers=headers)
    return response

def getSessionInfo():
    payload = "{\"method\":\"getSessionInfo\",\"params\":{}}"
    endpoint = "getSessionInfo"
    url = tab_server_url + "/vizportal/api/web/v1/"+endpoint
    print url
    headers = {
    'content-type': "application/json;charset=UTF-8",
    'accept': "application/json, text/plain, */*",
    'cache-control': "no-cache"
    }
    response = session.post(url, data=payload, headers=headers)
    return response.cookies


def generatePublicKey():
    payload = "{\"method\":\"generatePublicKey\",\"params\":{}}"
    endpoint = "generatePublicKey"
    url = tab_server_url + "/vizportal/api/web/v1/"+endpoint
    print url
    headers = {
    'content-type': "application/json;charset=UTF-8",
    'accept': "application/json, text/plain, */*",
    'cache-control': "no-cache"
    }
    response = session.post(url, data=payload, headers=headers)
    response_text = json.loads(_encode_for_display(response.text))
    # print response_text
    response_values = {"keyId":response_text["result"]["keyId"], "n":response_text["result"]["key"]["n"],"e":response_text["result"]["key"]["e"]}
    return response_values


def vizportalLogin(encryptedPassword, keyId):
    encodedPassword = binascii.b2a_hex(encryptedPassword)
    payload = "{\"method\":\"login\",\"params\":{\"username\":\"%s\", \"encryptedPassword\":\"%s\", \"keyId\":\"%s\"}}" % (tableau_username, encodedPassword,keyId)
    #print payload
    endpoint = "login"
    url = tab_server_url + "/vizportal/api/web/v1/"+endpoint
    #print url
    headers = {
    'content-type': "application/json;charset=UTF-8",
    'accept': "application/json, text/plain, */*",
    'cache-control': "no-cache"
    }
    response = session.post(url, data=payload, headers=headers)

# Encrypt with RSA public key (it's important to use PKCS11)
def assymmetric_encrypt(val, public_key):
    modulusDecoded = long(public_key["n"], 16)
    exponentDecoded = long(public_key["e"], 16)
    keyPub = RSA.construct((modulusDecoded, exponentDecoded))
    # Generate a cypher using the PKCS1.5 standard
    cipher = PKCS1_v1_5.new(keyPub)
    return cipher.encrypt(val)

if __name__ == '__main__':

    """ Generate Public Key
    This will be used to encrypt the user's password during login

    """
    public_key = generatePublicKey()
    print public_key

    """ Get the Session Info

    We need to retrieve the following values from the session cookies:

    workgroup_session_id
    XSRF-TOKEN

    """
    # cookie = requests.utils.dict_from_cookiejar(getSessionInfo())
    # print cookie

    pk = public_key["keyId"]
