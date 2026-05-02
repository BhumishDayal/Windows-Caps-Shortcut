from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from text_transformer import (  # noqa: E402
    ACRONYMS, BRANDS, repair, to_camel, to_snake, to_title, toggle_case,
)


def test_upper_basic():
    assert "hello world".upper() == "HELLO WORLD"


def test_lower_basic():
    assert "HELLO WORLD".lower() == "hello world"


def test_title_simple():
    assert to_title("hello world") == "Hello World"


def test_title_apostrophe_stays_in_word():
    assert to_title("don't stop") == "Don't Stop"


def test_title_treats_hyphen_as_boundary():
    assert to_title("re-write this") == "Re-Write This"


def test_title_treats_underscore_as_boundary():
    assert to_title("snake_case_words") == "Snake_Case_Words"


def test_title_collapses_existing_caps():
    assert to_title("HELLO WORLD") == "Hello World"


def test_title_canonicalizes_brands():
    assert to_title("typed on iphone") == "Typed On iPhone"
    assert to_title("built with javascript") == "Built With JavaScript"
    assert to_title("working at github") == "Working At GitHub"


def test_title_preserves_acronyms_case_insensitively():
    assert to_title("the gpu is hot") == "The GPU Is Hot"
    assert to_title("call the api endpoint") == "Call The API Endpoint"
    assert to_title("the GPU is hot") == "The GPU Is Hot"


def test_title_brand_with_punctuation():
    assert to_title("we love iphone, github") == "We Love iPhone, GitHub"


def test_title_recognizes_expanded_brands():
    assert to_title("built with fastapi") == "Built With FastAPI"
    assert to_title("deployed on next.js") == "Deployed On Next.js"
    assert to_title("we use openai") == "We Use OpenAI"
    assert to_title("running on macos") == "Running On macOS"
    assert to_title("via paypal") == "Via PayPal"


def test_title_recognizes_expanded_acronyms():
    assert to_title("the jwt expired") == "The JWT Expired"
    assert to_title("send via http") == "Send Via HTTP"
    assert to_title("the cdn is down") == "The CDN Is Down"
    assert to_title("the json response") == "The JSON Response"
    assert to_title("rsa key") == "RSA Key"
    assert to_title("via mqtt") == "Via MQTT"
    assert to_title("the dom tree") == "The DOM Tree"
    assert to_title("docker container with cron") == "Docker Container With Cron"


def test_repair_does_not_uppercase_lowercase_acronyms_in_prose():
    assert repair("the http call failed") == "the http call failed"


def test_acronym_list_excludes_common_english_words():
    # Regression guard - an acronym that's also a common English word would
    # corrupt Title Case in everyday prose.
    forbidden = {
        "IS", "IT", "AS", "OR", "ON", "AT", "BE", "BY", "DO", "GO",
        "HE", "IF", "IN", "ME", "MY", "NO", "OF", "SO", "TO", "UP",
        "US", "WE", "AM", "AN", "AND", "ARE", "BUT", "FOR", "NOT",
        "WAS", "THE", "REST", "SOAP", "WHO", "DRY", "KISS", "SOLID",
        "SAM", "ANN", "PAT", "TIM", "TOM", "BEN", "DAN", "ED", "MAX",
        "HID", "LED", "RAN", "SAW", "FED", "SET", "HAD", "HAS",
        "RADIUS", "ASP", "WORM", "YARN", "SPA", "SIP", "SAN", "TEE",
        "FAT", "POST", "POTS", "PROM", "RIP", "IDEA", "ELF", "ART",
        "APT", "ARM", "ATM", "MAN", "PAN", "TURN", "LISP",
    }
    leaked = forbidden & ACRONYMS
    assert not leaked, f"Dangerous English words leaked into ACRONYMS: {sorted(leaked)}"


def test_brand_list_no_duplicates_or_empty():
    assert "" not in BRANDS
    from text_transformer import DEFAULT_BRANDS
    assert len(set(DEFAULT_BRANDS)) == len(DEFAULT_BRANDS)


def test_toggle_swaps_each_letter():
    assert toggle_case("Hello World") == "hELLO wORLD"


def test_toggle_leaves_non_letters_alone():
    assert toggle_case("ABC 123 xyz") == "abc 123 XYZ"


def test_snake_from_spaces():
    assert to_snake("Hello World") == "hello_world"


def test_snake_from_camel():
    assert to_snake("camelCaseInput") == "camel_case_input"


def test_snake_from_pascal():
    assert to_snake("PascalCaseInput") == "pascal_case_input"


def test_snake_mixed_separators():
    assert to_snake("Mixed-Case_Input.Test") == "mixed_case_input_test"


def test_snake_collapses_repeats():
    assert to_snake("__double  spaces__") == "double_spaces"


def test_camel_from_spaces():
    assert to_camel("hello world") == "helloWorld"


def test_camel_from_snake():
    assert to_camel("snake_case_input") == "snakeCaseInput"


def test_camel_from_kebab():
    assert to_camel("kebab-case-input") == "kebabCaseInput"


def test_camel_lowercases_first_token_when_caps():
    assert to_camel("HELLO WORLD") == "helloWorld"


def test_camel_preserves_internal_camel_boundaries():
    assert to_camel("alreadyCamelHere") == "alreadyCamelHere"


def test_repair_signature_example():
    assert repair("mY NAME is jOHN dOE") == "My Name is John Doe"


def test_repair_caps_lock_shouting():
    assert repair("URGENT MEETING NOTES") == "Urgent Meeting Notes"


def test_repair_leaves_clean_lowercase_alone():
    assert repair("the quick brown fox") == "the quick brown fox"


def test_repair_preserves_acronyms_in_allowlist():
    assert repair("the GPU runs hot") == "the GPU runs hot"
    assert repair("call the API endpoint") == "call the API endpoint"


def test_repair_normalizes_typo_acronym():
    assert repair("the gPU runs hot") == "the Gpu runs hot"


def test_repair_canonicalizes_known_brands():
    assert repair("use github actions") == "use GitHub actions"
    assert repair("typed on iphone") == "typed on iPhone"
    assert repair("WRITTEN IN JAVASCRIPT") == "Written In JavaScript"


def test_repair_standalone_i_to_capital_I():
    assert repair("i think i can") == "I think I can"


def test_repair_leaves_urls_alone():
    assert repair("see https://Example.COM/path") == "see https://Example.COM/path"
    assert repair("ping mailto:Foo@bar.com") == "ping mailto:Foo@bar.com"


def test_repair_leaves_emails_alone():
    assert repair("write to Foo.Bar@example.com today") == \
           "write to Foo.Bar@example.com today"


def test_repair_leaves_code_identifiers_alone():
    assert repair("call get_user_name() now") == "call get_user_name() now"
    assert repair("the path is C:\\Foo\\bar") == "the path is C:\\Foo\\bar"


def test_repair_handles_punctuation_around_words():
    assert repair("hELLO, mR. jOHN dOE!") == "Hello, Mr. John Doe!"


def test_repair_empty_and_whitespace():
    assert repair("") == ""
    assert repair("   ") == "   "


def test_repair_preserves_whitespace_layout():
    assert repair("foo\t\tBAR\n\nbaz") == "foo\t\tBar\n\nbaz"


def test_empty_inputs():
    assert to_title("") == ""
    assert toggle_case("") == ""
    assert to_snake("") == ""
    assert to_camel("") == ""
    assert repair("") == ""


def test_whitespace_only():
    assert to_snake("   ") == ""
    assert to_camel("   ") == ""


def test_unicode_passthrough():
    assert to_title("café noir") == "Café Noir"
    assert toggle_case("Café") == "cAFÉ"
