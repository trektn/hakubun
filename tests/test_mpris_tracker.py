"""MprisTracker.on_filename_change: a player's reported duration
(mpris:length) must not be lost once a PropertiesChanged signal without
it arrives.

Regression coverage for a bug where handle_properties_changed() only
ever read mpris:length once, right when a player first connected
(Player.new() -> update_filename()). Any later PropertiesChanged signal
that changed the title/url (a new episode starting, or the player
finally reporting a duration it didn't know at connect time -- common,
since many players report metadata progressively as a file loads) went
through on_filename_change(), which never touched player.length at
all -- so a player whose duration wasn't known the instant it connected
never got one, permanently. That fed directly into two more visible
bugs: the Qt Now Playing progress bar could never show real progress
for such a player, and the mpris_obey_update_wait_s percentage-based
update toggle silently never activated (_percentage_wait_s() falls
back to the fixed wait whenever player.length is falsy).
"""

import asyncio
import time

from hakubun.tracker.mpris import MprisTracker, Player


def _bare_tracker():
    t = MprisTracker.__new__(MprisTracker)
    t.players = {}
    t.active_player = None
    return t


def _player(length=None):
    return Player(config={}, router=None, wellknown_name='org.mpris.MediaPlayer2.test',
                  unique_name=':1.1', length=length)


def test_length_is_set_when_reported_alongside_a_filename_change():
    t = _bare_tracker()
    player = _player(length=None)
    t.players[':1.1'] = player
    t._handle_player_update = lambda p: None

    t.on_filename_change(':1.1', 'Show', 'file:///show.mkv', 1400000)
    assert player.length == 1400000


def test_length_is_preserved_when_a_later_signal_omits_it():
    """A player that didn't know its duration when it first connected,
    then reports one later, then sends an unrelated title/url-only
    update -- the previously-learned length must survive that update."""
    t = _bare_tracker()
    player = _player(length=None)
    t.players[':1.1'] = player
    t._handle_player_update = lambda p: None

    # Connects with no duration known yet.
    t.on_filename_change(':1.1', 'Show', 'file:///show.mkv', None)
    assert player.length is None

    # Player reports the duration once it's finished probing the file.
    t.on_filename_change(':1.1', 'Show', 'file:///show.mkv', 1400000)
    assert player.length == 1400000

    # A later call with no length (e.g. the call site's real code only
    # forwards a length when metadata actually carried one) must not
    # wipe out the value already learned.
    t.on_filename_change(':1.1', 'Show', 'file:///show.mkv', None)
    assert player.length == 1400000


def test_length_updates_to_a_new_value_for_a_new_episode():
    t = _bare_tracker()
    player = _player(length=1400000)
    t.players[':1.1'] = player
    t._handle_player_update = lambda p: None

    t.on_filename_change(':1.1', 'Show', 'file:///show_ep2.mkv', 1450000)
    assert player.length == 1450000


class _SilentMsg:
    def __getattr__(self, name):
        return lambda *args, **kwargs: None


class _TickPlayer:
    """Minimal stand-in for an active Player during _on_tick()."""

    def __init__(self, length, position_us=0):
        self.length = length
        self._position_us = position_us
        self.wellknown_name = 'org.mpris.MediaPlayer2.test'

    async def get_position(self):
        return self._position_us


def _ticking_tracker(player, **config):
    t = MprisTracker.__new__(MprisTracker)
    t.players = {}
    t.active_player = player
    t.view_offset = None
    t.length = None
    t.wait_s = None
    t.last_show_tuple = None
    # Timer bookkeeping _percentage_wait_s reaches through
    # _effective_elapsed_s() once a playback position is known.
    t.last_time = time.time()
    t.timer_offset = 0
    t.timer_paused = None
    t.config = {'mpris_obey_update_wait_s': False,
                'tracker_update_percentage': 80,
                'tracker_update_wait_s': 120}
    t.config.update(config)
    return t


def test_on_tick_publishes_the_episode_duration_to_the_tracker():
    """The UI reads status['length'] (Tracker.get_status) to turn a
    playback position into a percentage. _on_tick() used to update
    view_offset but never self.length, so the tracker knew the position
    and the duration yet published only the former -- leaving the Now
    Playing progress bar permanently unable to show progress even
    though tracking itself worked fine."""
    player = _TickPlayer(length=1400000, position_us=700000000)
    t = _ticking_tracker(player)

    asyncio.run(t._on_tick())

    assert t.length == 1400000
    # Position is published in milliseconds, same unit as length.
    assert t.view_offset == 700000
    assert round(t.view_offset / t.length * 100) == 50


def test_stopping_clears_the_published_duration():
    """A stale length outliving the player it came from would let the
    bar show a percentage for nothing at all."""
    player = _TickPlayer(length=1400000)
    t = _ticking_tracker(player)
    asyncio.run(t._on_tick())
    assert t.length == 1400000

    t.msg = _SilentMsg()
    t.find_playing_player = lambda: True
    t._handle_player_stopped()

    assert t.length is None
    assert t.view_offset is None


def test_percentage_wait_follows_the_configured_percentage():
    """tracker_update_percentage replaces a hardcoded 0.80."""
    player = _TickPlayer(length=1400000)  # ms -> 1400s runtime

    t = _ticking_tracker(player, tracker_update_percentage=80)
    assert t._percentage_wait_s(player) == 1120

    t = _ticking_tracker(player, tracker_update_percentage=50)
    assert t._percentage_wait_s(player) == 700

    t = _ticking_tracker(player, tracker_update_percentage=95)
    assert t._percentage_wait_s(player) == 1330


def test_fixed_wait_toggle_still_overrides_the_percentage():
    player = _TickPlayer(length=1400000)
    t = _ticking_tracker(player, mpris_obey_update_wait_s=True,
                         tracker_update_percentage=50)
    assert t._percentage_wait_s(player) is None
