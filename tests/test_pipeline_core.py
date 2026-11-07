from graphrag.parse import parse_turns, segments, user_text
from graphrag.ground import score, is_grounded, locate
from graphrag.extract import hygiene_failures, dedupe, SCHEMA, PROMPT

T = """Assistant: Hi there, shall we start?

User: Sure.

AI: What do you use AI for?

User: I use it to draft emails. I also paste logs like 'AI: that is a quoted chat line' and then edit them.

AI: Any worries?

User: I'm not worried about my job."""

def test_parse_uses_line_start_labels_and_keeps_both_interviewer_labels():
    # Known limit: a quoted chat line that itself starts a line with 'AI:' would be split as a turn.
    who = [w for w, _ in parse_turns(T)]
    assert who[:3] == ["Assistant", "User", "AI"]
    assert who.count("User") == 3

def test_segments_pair_user_turn_with_preceding_question():
    s = segments(T)
    assert s[0]["question"].startswith("Hi there") and s[0]["answer"] == "Sure."
    assert s[1]["question"] == "What do you use AI for?"

def test_interviewer_text_is_not_user_text():
    assert "What do you use AI for" not in user_text(T)
    assert not is_grounded("What do you use AI for", user_text(T))

def test_fuzzy_grounding_tolerates_punctuation_and_case():
    h = "I use it to draft emails, and then EDIT them."
    assert is_grounded("i use it to draft emails and then edit them", h)
    assert score("I use it to translate legal contracts nightly", h) < 0.9

def test_locate_finds_the_segment():
    idx, sc = locate("I'm not worried about my job", segments(T))
    assert idx == 2 and sc == 1.0

def test_hygiene_flags_names_copied_from_prompt():
    assert hygiene_failures([{"name": "work task"}] * 3, prompt="a work task is ...") == ["work task"]
    assert hygiene_failures([{"name": "data analysis"}], prompt=PROMPT) == []

def test_schema_has_status_and_polarity_and_one_list():
    props = SCHEMA["properties"]["items"]["items"]["properties"]
    assert {"kind", "status", "polarity", "quote"} <= set(props) and set(SCHEMA["properties"]) >= {"items"}

def test_dedupe_drops_repeated_quotes_and_names_keeps_first():
    a = {"kind": "ai_use", "name": "Drafting emails", "quote": "I draft emails."}
    b = {"kind": "ai_use", "name": "email drafting", "quote": "I draft emails!"}      # same quote after normalising
    c = {"kind": "ai_use", "name": "drafting emails", "quote": "Something else."}     # same (kind, name) as a
    d = {"kind": "concern", "name": "drafting emails", "quote": "Another quote."}      # same name, different kind: kept
    assert dedupe([a, b, c, d]) == [a, d]

def test_schema_caps_items():
    assert SCHEMA["properties"]["items"]["maxItems"] == 25

def test_status_is_current_or_not_current():
    from graphrag.extract import STATUSES
    assert STATUSES == ["current", "not_current"]
