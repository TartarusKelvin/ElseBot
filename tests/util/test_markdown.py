import pytest
import else_bot.util.markdown as markdown


def test_links():
    text = "Hello everyone, welcome to Bottom Five! Listen, at some point you need to just stop trying to balance it. Let's get to it!\n\nThis week's [album](https://imgur.com/a/4oblxdl).\n\n\n1. [Ancestral Confluence](https://dr.reddit.com/r/custommagic/comments/17rwmrf/this_is_probably_still_broken/) by /u/Due-Try1107\n\n\n\n2. [The Urborg Masses](https://dr.reddit.com/r/custommagic/comments/17qfaze/the_urborg_masses/) by /u/Vi0letBlues\n\n\n3. [Yubitsume](https://dr.reddit.com/r/custommagic/comments/17t6nkw/yubitsume/) by /u/Right-Charge5361\n\n4. [Oppressive Landlord](https://dr.reddit.com/r/custommagic/comments/17qo7ik/oppressive_landlord_trying_to_punish_land_ramp/) by /u/Islarf\n\n\n5. [Death's Whisper](https://dr.reddit.com/r/custommagic/comments/17sb5qu/just_a_random_card_i_thought_of/) by /u/Confident_End3951\n\n\n\nDishonorable Mentions:\n\n1. [Grack the Trampler](https://dr.reddit.com/r/custommagic/comments/17rkbk8/indestructible_tribal_grack_the_trampler/) by /u/Lvl_76_Pyromancer\n\n\n2. [Inconstant Necrophiliac](https://dr.reddit.com/r/custommagic/comments/17u5qdm/inconstant_necrophiliac/) by /u/RedKing85\n\n3. [Mauga, Heavy Assault](https://dr.reddit.com/r/custommagic/comments/17so9se/ready_to_have_some_fun_i_still_really_dont_like/) by /u/Biggieboy4114\n\n\n\nYou can find last week's thread [here](https://dr.reddit.com/r/magicthecirclejerking/comments/17q7o59/bottom_5_scoring_submissions_of_the_week_from/) \nand the Top 5 submissions [here](https://dr.reddit.com/r/magicTCG/comments/17v0qmz/top_5_scoring_submissions_of_the_week_from/)."
    links = markdown.get_links(text)
    assert len(links) == 11
    link_names = [
        "album",
        "Ancestral Confluence",
        "The Urborg Masses",
        "Yubitsume",
        "Oppressive Landlord",
        "Death's Whisper",
        "Grack the Trampler",
        "Inconstant Necrophiliac",
        "Mauga, Heavy Assault",
        "here",
        "here",
    ]
    for x in zip(link_names, [x[0] for x in links]):
        assert x[0] == x[1], "Incorrect link name"
