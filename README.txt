PowerAdminCoD7 plugin for Big Brother Bot (www.bigbrotherbot.net)
===================================================================

Author: Freelander - freelander@bigbrotherbot.net
Author URI: http://www.bigbrotherbot.net
Author URI: http://www.fps-gamer.net

Description
-----------

This plugin adds some extra functionality to B3 in both ranked and unranked 
CoD:Blackops servers.

Commands
--------

Ranked servers only:
 !pasetmap <mapname> - Set the next map in rotation

Ranked/Unranked servers:
 !paplaylist - Display current playlist
 !pagetplaylists - Display available playlists
 !pasetplaylist <playlist_number> - Set a playlist
 !paexcludemaps <maps> - Excludes entered maps from rotation. Example: !paexludemaps mp_villa mp_nuked mp_array
 !paversion - Identifies PowerAdminCoD7 version and creator
 !paident [<playername>] - Show the ip and guid of a player
 !paset <cvar> <value> - Set a server cvar to a certain value
 !paget <cvar> - Returns the value of a server cvar
 !pasetdlc <dlc number> <on | off> - Turn given DLC mappack on or off. Example: !pasetdlc 1 off.
 !palistcfg - List available server config files in b3 conf folder
 !paload <configfile.cfg> - Load a server configfile.

Unranked servers only:
 !pafastrestart - Restart current map without reloading it
 !pamaprestart - Restart current map
 !pagametype <gametype> - Change gametype. Example: !gametype tdm

Changelog
---------

 * 19.04.2011 - v1.0
    - Initial release
 * 02.06.2011 - v1.1
    - DLC2 maps added
 * 09.06.2011 - 1.2
    - !pasetmap (!setmap) command now works both with console map names and easy map names
      as well as console map name without "mp_" at the beginning. (as printed out
      by !maps command)
    - Added new commands !pasetdlc, !palistcfg and !paloadcfg


Installation
------------

 * copy poweradmincod7.py into b3/extplugins
 * copy plugin_poweradmincod7.xml into your b3/extplugins/conf folder
 * edit plugin_poweradmincod7.xml with your preferred settings
 * update your main b3 config file with :
   <plugin name="poweradmincod7" config="@b3/extplugins/conf/plugin_poweradmincod7.xml"/>

Notes
-----
 If you're loading a config file using !paload command, it may take a while to load the
 complete file depending on the file size. Note that, during the loading process, other B3 commands
 issued will be queued but they may timeout. Hence it is NOT recommended to load config files in peak
 server times.
 
Support
-------

see the B3 forums http://forum.bigbrotherbot.net/releases/poweradmincod7/