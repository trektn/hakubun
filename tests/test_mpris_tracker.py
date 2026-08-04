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
