# Copyright (C) 2012-2018 The python-bitcoinlib developers
# Copyright (C) 2018 The python-bitcointx developers
#
# This file is part of python-bitcointx.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

import bitcointx.core

# Note that setup.py can break if __init__.py imports any external
# dependencies, as these might not be installed when setup.py runs. In this
# case __version__ could be moved to a separate version.py and imported here.
__version__ = '0.10.2.dev1'


class MainParams(bitcointx.core.CoreMainParams):
    RPC_PORT = 8332
    BASE58_PREFIXES = {'PUBKEY_ADDR':0,
                       'SCRIPT_ADDR':5,
                       'SECRET_KEY' :128}
    BECH32_HRP = 'bc'


class TestNetParams(bitcointx.core.CoreTestNetParams):
    RPC_PORT = 18332
    BASE58_PREFIXES = {'PUBKEY_ADDR':111,
                       'SCRIPT_ADDR':196,
                       'SECRET_KEY' :239}
    BECH32_HRP = 'tb'


class RegTestParams(bitcointx.core.CoreRegTestParams):
    RPC_PORT = 18443
    BASE58_PREFIXES = {'PUBKEY_ADDR':111,
                       'SCRIPT_ADDR':196,
                       'SECRET_KEY' :239}
    BECH32_HRP = 'bcrt'

"""Master global setting for what chain params we're using.

However, don't set this directly, use SelectParams() instead so as to set the
bitcointx.core.params correctly too.
"""
params = MainParams()


def SelectAlternativeParams(alt_core_params, alt_main_params):
    """Select alternative chain parameters to use

    alt_core_params should be a subclass of core.CoreChainParams,
    but redefine all fields

    alt_main_params should be a subclass of alt_core_params,
    and define all fields that are defined in MainParams

    """
    global params

    bitcointx.core._SelectAlternativeCoreParams(alt_core_params)

    assert(issubclass(alt_main_params, alt_core_params))

    param_names = set([pn for pn in alt_main_params.__dict__
                       if not pn.startswith('_')])
    required_param_names = set([pn for pn in MainParams.__dict__
                                if not pn.startswith('_')])

    assert(len(param_names) >= len(required_param_names)
           and len(required_param_names - param_names) == 0),\
        ("alternative params should specify all fields defined in "
         "MainParams, but {} are undefined"
         .format(required_param_names - param_names))

    params = alt_main_params


def SelectParams(name):
    """Select the chain parameters to use

    name is one of 'mainnet', 'testnet', or 'regtest'

    Default chain is 'mainnet'
    """
    global params
    bitcointx.core._SelectCoreParams(name)
    if name == 'mainnet':
        params = bitcointx.core.coreparams = MainParams()
    elif name == 'testnet':
        params = bitcointx.core.coreparams = TestNetParams()
    elif name == 'regtest':
        params = bitcointx.core.coreparams = RegTestParams()
    else:
        raise ValueError('Unknown chain %r' % name)
