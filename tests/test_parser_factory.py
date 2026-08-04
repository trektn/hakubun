from hakubun.messenger import Messenger
from hakubun.parser import get_parser_class
from hakubun.parser.animeinfoextractor import AnimeInfoExtractor
from hakubun.parser.anitopy import AnitopyWrapper

_msg = Messenger(None, 'Tests')


def test_aie_is_selectable():
    assert get_parser_class(_msg, 'aie') is AnimeInfoExtractor


def test_anitopy_is_selectable():
    assert get_parser_class(_msg, 'anitopy') is AnitopyWrapper


def test_anitomy_ng_is_selectable():
    import pytest
    pytest.importorskip('anitomy_ng')
    from hakubun.parser.anitomy_ng import AnitomyNgWrapper
    assert get_parser_class(_msg, 'anitomy_ng') is AnitomyNgWrapper


def test_unknown_parser_name_falls_back_to_aie():
    """Regression: the fallback branch called get_parser_class('aie') with
    only one positional argument, so an unrecognized title_parser value in
    an existing config raised TypeError (missing 'parser_name') instead of
    falling back as intended."""
    assert get_parser_class(_msg, 'not_a_real_parser') is AnimeInfoExtractor
