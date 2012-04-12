# -*- coding: utf-8 -*-

from datetime import datetime
from operator import itemgetter
import utils

__author__ = "Arun KR (kra3) <the1.arun@gmail.com>"
__license__ = "Simplified BSD"

class Campaign(object):
    pass


class CustomVariable(object):
    pass


class Event(object):
    pass


class Item(object):
    '''
    Represents an Item in Transaction

    Properties:
    order_id -- Order ID, will be mapped to "utmtid" parameter
    sku -- Product Code. This is the sku code for a given product, will be mapped to "utmipc" parameter
    name -- Product Name, will be mapped to "utmipn" parameter
    variation -- Variations on an item, will be mapped to "utmiva" parameter
    price -- Unit Price. Value is set to numbers only, will be mapped to "utmipr" parameter
    quantity -- Unit Quantity, will be mapped to "utmiqt" parameter

    '''

    def __init__(self):
        self.order_id = None
        self.sku = None
        self.name = None
        self.variation = None
        self.price = None
        self.quantity = 1

    def validate(self):
        if not self.sku:
            raise Exception('sku/product is a required parameter')


class Page(object):
    '''
    Contains all parameters needed for tracking a page

    Properties:
    path -- Page request URI, will be mapped to "utmp" parameter
    title -- Page title, will be mapped to "utmdt" parameter
    charset -- Charset encoding, will be mapped to "utmcs" parameter
    referrer -- Referer URL, will be mapped to "utmr" parameter
    load_time -- Page load time in milliseconds, will be encoded into "utme" parameter.

    '''
    REFERRER_INTERNAL = '0'

    def __init__(self, path):
        self.path = None
        self.title = None
        self.charset = None
        self.referrer = None
        self.load_time = None

        if path_val:
            self.path= path

    def __setattr__(self, name, value):
        if name == 'path':
            if value and value != '':
                if value[0] != '/':
                    raise Exception('The page path should always start with a slash ("/").')
        elif name == 'load_time':
            if value and not isinstance(value, int):
                raise Exception('Page load time must be specified in integer milliseconds.')

        object.__setattr__(self, name, value)


class Session(object):
    '''
    You should serialize this object and store it in the user session to keep it
    persistent between requests (similar to the "__umtb" cookie of the GA Javascript client).

    Properties:
    session_id -- A unique per-session ID, will be mapped to "utmhid" parameter
    track_count -- The amount of pageviews that were tracked within this session so far,
                   will be part of the "__utmb" cookie parameter.
                   Will get incremented automatically upon each request
    start_time -- Timestamp of the start of this new session, will be part of the "__utmb" cookie parameter

    '''
    def __init__(self):
        self.session_id = utils.get_32bit_random_num()
        self.track_count = 0
        self.start_time = datetime.now()

    @staticmethod
    def generate_session_id():
        return utils.get_32bit_random_num()

    def extract_from_utmb(self, utmb):
        '''
        Will extract information for the "trackCount" and "startTime"
        properties from the given "__utmb" cookie value.
        '''
        parts = utmb.split('.')
        if len(parts) != 4:
            raise Exception('The given "__utmb" cookie value is invalid.')

        self.track_count = parts[1]
        self.start_time = datetime.fromtimestamp(parts[3])

        return self


class SocialInteraction(object):
    pass


class Tracker(object):
    VERSION = '5.2.5' # As of 25.02.2012
    pass


class Transaction(object):
    '''
    Represents parameters for a Transaction call

    Properties:
    order_id -- Order ID, will be mapped to "utmtid" parameter
    affiliation -- Affiliation, Will be mapped to "utmtst" parameter
    total -- Total Cost, will be mapped to "utmtto" parameter
    tax -- Tax Cost, will be mapped to "utmttx" parameter
    shipping -- Shipping Cost, values as for unit and price, will be mapped to "utmtsp" parameter
    city -- Billing City, will be mapped to "utmtci" parameter
    state -- Billing Region, will be mapped to "utmtrg" parameter
    country -- Billing Country, will be mapped to "utmtco" parameter
    items -- @entity.Items in a transaction

    '''
    def __init__(self):
        self.order_id = None
        self.affiliation = None
        self.total = None
        self.tax = None
        self.shipping = None
        self.city = None
        self.state = None
        self.country = None
        self.items = []

    def __setattr__(self, name, value):
        if name == 'order_id':
            for itm in items:
                itm.order_id = value
        object.__setattr__(self, name, value)

    def validate(self):
        if len(items) == 0:
            raise Exception('Transaction need to consist of at least one item')

    def add_item(self, item):
        ''' item of type entities.Item '''
        item.order_id = self.order_id
        self.items.append(item)


class Visitor(object):
    '''
    You should serialize this object and store it in the user database to keep it
    persistent for the same user permanently (similar to the "__umta" cookie of
    the GA Javascript client).

    Parameters:
    unique_id -- Unique user ID, will be part of the "__utma" cookie parameter
    first_visit_time -- Time of the very first visit of this user, will be part of the "__utma" cookie parameter
    previous_visit_time -- Time of the previous visit of this user, will be part of the "__utma" cookie parameter
    current_visit_time -- Time of the current visit of this user, will be part of the "__utma" cookie parameter
    visit_count -- Amount of total visits by this user, will be part of the "__utma" cookie parameter
    ip_address -- IP Address of the end user, will be mapped to "utmip" parameter and "X-Forwarded-For" request header
    user_agent -- User agent string of the end user, will be mapped to "User-Agent" request header
    locale -- Locale string (country part optional) will be mapped to "utmul" parameter
    flash_version -- Visitor's Flash version, will be maped to "utmfl" parameter
    java_enabled -- Visitor's Java support, will be mapped to "utmje" parameter
    screen_colour_depth -- Visitor's screen color depth, will be mapped to "utmsc" parameter
    screen_resolution -- Visitor's screen resolution, will be mapped to "utmsr" parameter
    '''
    def __init__(self):
        now = datetime.now()

        self.unique_id = None
        self.first_visit_time = now
        self.previous_visit_time = now
        self.current_visit_time = now
        self.visit_count = 1
        self.ip_address = None
        self.user_agent = None
        self.locale = None
        self.flash_version = None
        self.java_enabled = None
        self.screen_colour_depth = None
        self.screen_resolution = None

    def __setattr__(self, name, value):
        if name == 'unique_id':
            if value and value < 0 or value > 0x7fffffff:
                raise Exception('Visitor unique ID has to be a 32-bit integer between 0 and 0x7fffffff')
        object.__setattr__(self, name, value)

    def __getattribute__(self, name):
        if name == 'unique_id':
            tmp = object.__getattribute__(self, name)
            if tmp == None:
                self.unique_id = self.generate_unique_id()
        return object.__getattribute__(self, name)

    def extract_from_utma(self, utma):
        '''
        Will extract information for the "unique_id", "first_visit_time", "previous_visit_time",
        "current_visit_time" and "visit_count" properties from the given "__utma" cookie value.
        '''
        parts = utma.split('.')
        if len(parts) != 6:
            raise Exception('The given "__utma" cookie value is invalid.')

        self.unique_id = parts[1]
        self.first_visit_time = datetime.fromtimestamp(parts[2])
        self.previous_visit_time = datetime.fromtimestamp(parts[3])
        self.current_visit_time = datetime.fromtimestamp(parts[4])
        self.visit_count = parts[5]

        return self

    def extract_from_server_meta(self, meta):
        '''
        Will extract information for the "ip_address", "user_agent" and "locale"
        properties from the given WSGI REQUEST META variable or equivalent.
        '''
        if meta.has_key('REMOTE_ADDR') and meta['REMOTE_ADDR']:
            ip = None
            for key in ('X_FORWARDED_FOR', 'REMOTE_ADDR'):
                if meta.has_key(key) and not ip:
                    ips = meta.get(key, '').split(',')
                    ip = ips[len(ips)-1].strip()
                    if not utils.is_valid_ip(ip):
                        ip = None
                    if utils.is_private_ip(ip):
                        ip = None
            if ip:
                self.ip_address = ip

        if meta.has_key('HTTP_USER_AGENT') and meta['HTTP_USER_AGENT']:
            self.user_agent = meta['HTTP_USER_AGENT']

        if meta.has_key('HTTP_ACCEPT_LANGUAGE') and meta['HTTP_ACCEPT_LANGUAGE']:
            user_locals = []
            matched_locales = utils.validate_locale(meta['HTTP_ACCEPT_LANGUAGE'])
            if matched_locales:
                lang_lst = map((lambda x: x.replace('-', '_')), (i[1] for i in matched_locales))
                quality_lst = map((lambda x: x and x or 1), (float(i[4]) for i in matched_locales))
                lang_quality_map = map((lambda x,y: (x,y)), lang_lst, quality_lst)
                user_locals = [x[0] for x in sorted(lang_quality_map, key=itemgetter(1), reverse=True)]

            if user_locals:
                self.locale = user_locals[0]

        return self

    def generate_hash(self):
        '''Generates a hashed value from user-specific properties.'''
        tmpstr = "%s%s%s" % (self.user_agent, self.screen_resolution, self.screen_colour_depth)
        return utils.generate_hash(tmpstr)

    def generate_unique_id(self):
        '''Generates a unique user ID from the current user-specific properties.'''
        return ((utils.get_32bit_random_num() ^ self.generate_hash()) & 0x7fffffff)

    def add_session(self, session):
        '''
        Updates the "previousVisitTime", "currentVisitTime" and "visitCount"
        fields based on the given session object.
        '''
        start_time = session.start_time
        if start_time != self.current_visit_time:
            self.previous_visit_time = self.current_visit_time
            self.current_visit_time = start_time
            self.visit_count = self.visit_count + 1
