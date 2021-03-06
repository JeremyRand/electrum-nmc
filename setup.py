#!/usr/bin/env python3

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp
import argparse

with open('contrib/requirements/requirements.txt') as f:
    requirements = f.read().splitlines()

with open('contrib/requirements/requirements-hw.txt') as f:
    requirements_hw = f.read().splitlines()

version = imp.load_source('version', 'lib/version.py')

if sys.version_info[:3] < (3, 4, 0):
    sys.exit("Error: Electrum requires Python version >= 3.4.0...")

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    icons_dirname = 'pixmaps'
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        icons_dirname = 'icons'
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['electrum-nmc.desktop']),
        (os.path.join(usr_share, icons_dirname), ['icons/electrum.png'])
    ]

setup(
    name="Electrum-NMC",
    version=version.ELECTRUM_VERSION,
    install_requires=requirements,
    extras_require={
        'full': requirements_hw + ['pycryptodomex'],
    },
    packages=[
        'electrum_nmc',
        'electrum_nmc_gui',
        'electrum_nmc_gui.qt',
        'electrum_nmc_plugins',
        'electrum_nmc_plugins.audio_modem',
        'electrum_nmc_plugins.cosigner_pool',
        'electrum_nmc_plugins.email_requests',
        'electrum_nmc_plugins.greenaddress_instant',
        'electrum_nmc_plugins.hw_wallet',
        'electrum_nmc_plugins.keepkey',
        'electrum_nmc_plugins.labels',
        'electrum_nmc_plugins.ledger',
        'electrum_nmc_plugins.trezor',
        'electrum_nmc_plugins.digitalbitbox',
        'electrum_nmc_plugins.trustedcoin',
        'electrum_nmc_plugins.virtualkeyboard',
    ],
    package_dir={
        'electrum_nmc': 'lib',
        'electrum_nmc_gui': 'gui',
        'electrum_nmc_plugins': 'plugins',
    },
    package_data={
        'electrum_nmc': [
            'servers.json',
            'servers_testnet.json',
            'servers_regtest.json',
            'currencies.json',
            'checkpoints.json',
            'checkpoints_testnet.json',
            'www/index.html',
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/electrum.mo',
        ]
    },
    scripts=['electrum-nmc'],
    data_files=data_files,
    description="Lightweight Namecoin Wallet",
    author="Namecoin Developers; Based on Electrum by Thomas Voegtlin",
    author_email="jeremy@namecoin.org",
    license="MIT Licence",
    url="https://www.namecoin.org",
    long_description="""Lightweight Namecoin Wallet"""
)
