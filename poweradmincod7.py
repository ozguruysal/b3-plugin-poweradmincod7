#
# PowerAdmin Plugin for BigBrotherBot(B3) (www.bigbrotherbot.com)
# Copyright (C) 2005 www.xlr8or.com
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# Changelog:
# * 10.04.2011 - 1.0
#   - Initial release
# * 02.06.2011 - 1.1
#   - DLC2 Changes
#

__version__ = '1.1'
__author__  = 'Freelander'

import b3, re
import b3.events
import time

class Poweradmincod7Plugin(b3.plugin.Plugin):
    _adminPlugin = None
    _isranked = None
    _issetmap = False
    _isplaylist_enabled = True
    _admin_excluded_maps = None
    _cod7maps = { 
                  'mp_array' : 'Array',
                  'mp_cracked' : 'Cracked',
                  'mp_crisis' : 'Crisis',
                  'mp_firingrange' : 'Firing Range',
                  'mp_duga' : 'Grid',
                  'mp_hanoi' : 'Hanoi',
                  'mp_cairo' : 'Havana',
                  'mp_havoc' : 'Jungle',
                  'mp_cosmodrome' : 'Launch',
                  'mp_nuked' : 'Nuketown',
                  'mp_radiation' : 'Radiation',
                  'mp_mountain' : 'Summit',
                  'mp_villa' : 'Villa',
                  'mp_russianbase' : 'WMD',
                  'mp_berlinwall2' : 'Berlin Wall',
                  'mp_discovery' : 'Discovery',
                  'mp_kowloon' : 'Kowloon',
                  'mp_stadium' : 'Stadium',
                  'mp_convoy' : 'Convoy',
                  'mp_hotel' : 'Hotel',
                  'mp_stockpile' : 'Stockpile',
                  'mp_zoo' : 'Zoo'
                }

    _playlists = {
                   1  : 'Team Deathmatch',
                   2  : 'Free For All',
                   3  : 'Capture The Flag',
                   4  : 'Search & Destroy',
                   5  : 'Headquarters',
                   6  : 'Domination',
                   7  : 'Sabotage',
                   8  : 'Demolition',
                   9  : 'Hardcore Team Deathmatch',
                   10 : 'Hardcore Free For All',
                   11 : 'Hardcore Capture The Flag',
                   12 : 'Hardcore Search & Destroy',
                   13 : 'Hardcore Headquarters',
                   14 : 'Hardcore Domination',
                   15 : 'Hardcore Sabotage',
                   16 : 'Hardcore Demolition',
                   17 : 'Barebones Team Deathmatch',
                   18 : 'Barebones Free For All',
                   19 : 'Barebones Capture The Flag',
                   20 : 'Barebones Search & Destroy',
                   21 : 'Barebones Headquarters',
                   22 : 'Barebones Domination',
                   23 : 'Barebones Sabotage',
                   24 : 'Barebones Demolition',
                   25 : 'Team Tactical'
                 }

    #---------------------------------------------------------------------------------

    def onStartup(self):
        '''\
        Initialize plugin settings
        '''
        # get the admin plugin so we can register commands
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            # something is wrong, can't start without admin plugin
            self.error('Could not find admin plugin')
            return False

        # register our commands
        self._registerCommands()

        # check if server is ranked/unranked
        self._isranked = self.isranked()
        if self._isranked:
            self.debug('This server is Ranked')
        else:
            self.debug('This server is Unranked')
            # check playlist status
            self._isplaylist_enabled = self.isplaylist_enabled()

        # get maplist excluded by server admin
        m = self.console.getCvar('playlist_excludeMap')
        if m and m != '':
            self._admin_excluded_maps = m.value
            if self._admin_excluded_maps != '':
                self.debug('Excluded maps by admin are: %s' % self._admin_excluded_maps)
            else:
                self.debug('No maps found in map exclusion list')

    def getCmd(self, cmd):
        cmd = 'cmd_%s' % cmd
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            return func
        return None

    def _registerCommands(self):
        # register our commands
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp
                func = self.getCmd(cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)

        # Register our events
        self.verbose('Registering events')
        self.registerEvent(b3.events.EVT_GAME_ROUND_START)

    def onEvent(self, event):
        '''\
        Handle intercepted events
        '''
        if event.type == b3.events.EVT_GAME_ROUND_START:
            if self._issetmap:
                self.console.write ('setadmindvar playlist_excludeMap "%s"' % self._admin_excluded_maps, maxRetries=5)
                self._issetmap = False
                self.debug ('Clearing map exclusion list')

    #---------------------------------------------------------------------------------

    def cmd_paplaylist(self, data, client, cmd):
        '''\
        Display current playlist.
        (You can safely use the command without the 'pa' at the beginning)
        '''
        cvar = self.console.getCvar('playlist')
        if cvar:
            playlist = cvar.getInt()
        else:
            return

        cmd.sayLoudOrPM(client, '^7Current Playlist is ^3%s - %s' % (playlist, self._playlists[playlist]))

    def cmd_pagetplaylists(self, data, client, cmd):
        '''\
        Display available playlists
        (You can safely use the command without the 'pa' at the beginning)
        '''
        for n, p in sorted(self._playlists.iteritems()):
            cmd.sayLoudOrPM(client, '%s - %s' % (n, p))
            time.sleep(1)

    def cmd_pasetplaylist(self, data, client, cmd):
        '''\
        <playlist_number> - Set a playlist
        (You can safely use the command without the 'pa' at the beginning)
        '''
        if not self._isplaylist_enabled and not self._isranked:
            client.message('Playlists are not enabled in this server. You can\'t set a playlist!')
            return False

        _number_of_playlists = len(self._playlists)

        if not data:
            client.message('missing parameter, try !help pasetplaylist')
            return False
        else:
            try:
                float(data)
            except ValueError:
                client.message('Please use a playlist number, %s is not a numeric value' % data)
                return False

        data = int(data)
        if data not in range(1, _number_of_playlists + 1):
            client.message('Playlist number %s out of range! Please enter a valid number' % data)
        else:
            self.console.write('setadmindvar playlist %s' % data, maxRetries=5)
            client.message('Changing playlist to ^3%s - %s' % (data, self._playlists[data]))

    def cmd_pasetmap(self, data, client, cmd=None):
        '''\
        <mapname> - Set the next map in rotation
        (You can safely use the command without the 'pa' at the beginning)
        '''
        if not self._isranked:
            client.message('This command is not functional in unranked servers. You can use ^2!map ^7or ^2!maprotate ^7 commands instead.')
            return False

        if not data:
            client.message('missing parameter, try !help pasetmap')
            return False
        else:
            data = data.split(' ')
            mapname = data[0].lower()
            if mapname.startswith('mp_'):
                mapname = mapname
            else:
                mapname = ('mp_%s' % mapname)

            self.debug('Requested map for next round is %s' % mapname)

            if mapname not in self._cod7maps:
                client.message('%s is not a stock CoD7 map, please check your spelling and try again!' % mapname)
                return False
            else:
                excludeMaps = self._cod7maps.keys()
                excludeMaps.remove(mapname)
                self.console.write('setadmindvar playlist_excludeMap "%s"' % ' '.join(excludeMaps), maxRetries=5)
                client.message('Setting map ^3%s for next round' % self._cod7maps[mapname])
                self._issetmap = True

    def cmd_paexcludemaps(self, data, client, cmd=None):
        '''\
        <mapnames> Excludes entered maps from rotation. 
        Leave a space between mapnames. Example: !paexludemaps mp_villa mp_nuked mp_array
        (You can safely use the command without the 'pa' at the beginning)
        '''
        if not self._isplaylist_enabled and not self._isranked:
            client.message('Playlists are not enabled in this server. You can\'t make an exclusion list!')
            return False

        if not data:
            client.message('missing parameter, try !help pasetplaylist')
            return False
        else:
            #check if mapnames typed correctly
            mapnames = data.split(' ')
            for m in mapnames:
                if m not in self._cod7maps.keys():
                    client.message('%s is not a valid mapname, please check your spelling and try again' % m)
                    return False

            self.console.write('setadmindvar playlist_excludeMap "%s"' % data, maxRetries=5)
            #updating exclusion list variable
            self._admin_excluded_maps = data
            self.debug('Maps: %s excluded from current playlist' % mapnames)

    def cmd_paversion(self, data, client, cmd=None):
        '''\
        This command identifies PowerAdminCoD7 version and creator.
        '''
        #client.message(message)
        cmd.sayLoudOrPM(client, 'I am PowerAdminCoD7 version %s by %s' % (__version__, __author__))
        return None

    def cmd_paident(self, data, client, cmd=None):
        '''\
        [<name>] - show the ip and guid of a player
        '''
        input = self._adminPlugin.parseUserCmd(data)
        if not input:
            # assume the player wants his own ident
            try:
                cmd.sayLoudOrPM(client, '%s: %s - %s' % (client.name, client.ip, client.guid))
            except Exception, err:
                client.message('Error, server replied %s' % err)
        else:
            try:
                # input[0] is the player id
                sclient = self._adminPlugin.findClientPrompt(input[0], client)
                if sclient:
                    cmd.sayLoudOrPM(client, '%s: %s - %s' % (sclient.name, sclient.ip, sclient.guid))
            except Exception, err:
                client.message('Error, server replied %s' % err)

    def cmd_paset(self, data, client, cmd=None):
        '''\
        <cvar> <value> - Set a server cvar to a certain value.
        (You must use the command exactly as it is! )
        '''
        if not data:
            client.message('^7Invalid or missing data, try !help paset')
            return False
        else:
            # are we still here? Let's write it to console
            input = data.split(' ',1)
            cvarName = input[0].lower()
            value = input[1]
            self.console.setCvar(cvarName, value)
            client.message('Setting %s to %s' % (cvarName, value))

            # check if we are setting a new map exclusion list
            # then we'll need to update exclusion list made by server admin
            if cvarName.lower() == 'playlist_excludemap':
                self._admin_excluded_maps = value

        return True

    def cmd_paget(self, data, client, cmd=None):
        '''\
        <cvar> - Returns the value of a servercvar.
        (You must use the command exactly as it is! )
        '''
        if not data:
            client.message('^7Invalid or missing data, try !help paget')
            return False
        else:
            # are we still here? Let's write it to console
            getcvar = data.split(' ')
            getcvarvalue = self.console.getCvar( '%s' % getcvar[0] )
            cmd.sayLoudOrPM(client, '%s' % getcvarvalue)

        return True

    def cmd_pafastrestart(self, data, client, cmd):
        '''
        Restart a map without reloading it
        (You can safely use the command without the 'pa' at the beginning)
        '''
        if self._isranked:
            client.message('You can\'t restart a map on ranked servers')
            return False
        else:
            self.console.say('Fast restarting map in 2 seconds...')
            time.sleep(2)
            self.console.write('fast_restart', maxRetries=5)
            return True

    def cmd_pamaprestart(self, data, client, cmd):
        '''
        Restart a map
        (You can safely use the command without the 'pa' at the beginning)
        '''
        if self._isranked:
            client.message('You can\'t restart a map on ranked servers')
            return False
        else:
            self.console.say('Restarting map in 2 seconds...')
            time.sleep(2)
            self.console.write('map_restart', maxRetries=5)
            return True

    def cmd_pagametype(self, data, client, cmd):
        '''
        <gametype> Change gametype. Example: !gametype tdm
        (You can safely use the command without the 'pa' at the beginning)
        '''
        if self._isranked:
            client.message('This command is not available on ranked servers!')
            return False

        gametypes = { 
                      'dm' : 'Free-For-All',
                      'tdm' : 'Team Deathmatch',
                      'sd' : 'Search and Destroy',
                      'dom' : 'Domination',
                      'sab' : 'Sabotage',
                      'ctf' : 'Capture the Flag',
                      'koth' : 'Headquarters',
                      'dem' : 'Demolition',
                      'oic' : 'One in the Chamber',
                      'hlnd' : 'Sticks and Stones',
                      'gun' : 'Gun Game',
                      'shrp' : 'Sharpshooter'
                     }

        if not data:
            client.message('missing parameter, try !help pagametype')
            return False
        else:
            #check if gametype is valid
            data = data.split(' ')
            gametype = data[0].lower()
            for g in gametypes:
                if gametype not in gametypes.keys():
                    client.message('^3%s ^7is not a valid gametype, please try again!' % gametype)
                    return False

            self.console.say('Changing gametype to %s, map will restart in 5 seconds' % gametypes[gametype])
            self.console.write('g_gametype %s' % gametype, maxRetries=5)
            time.sleep(5)
            self.console.write('map_restart', maxRetries=5)

    #---------------------------------------------------------------------------------

    def isranked(self):
        '''\
        Returns true if server is ranked
        '''
        rank = self.console.getCvar('sv_ranked')

        if rank:
            if rank.getInt() == 2:
                return True
            else:
                return False
        else:
            return None

    def isplaylist_enabled(self):
        '''\
        Returns true if playlists are enabled
        '''
        status = self.console.getCvar('playlist_enabled')

        if status:
            if status.getBoolean():
                self.debug('Playlist Enabled')
                return True
            else:
                self.debug('Playlist Disabled')
                return False
