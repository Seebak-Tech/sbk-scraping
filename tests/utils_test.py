import pytest
import json
from pathlib import Path
from sbk_scraping.utils import (
    ensure_path_exists,
    load_json_file,
    read_parsers
)


def test_ensure_path_exists():
    invalid_path = Path('/otro')
    with pytest.raises(
            ValueError,
            match='Validate the following'
    ):
        _ = ensure_path_exists(invalid_path)


def test_read_parsers(config):
    data = read_parsers(config)
    assert len(data) != 0
    assert isinstance(data, dict)


def test_invalid_content_jsonfile(test_data):
    with pytest.raises(
        json.decoder.JSONDecodeError,
        match='Expecting value'
    ):
        _ = load_json_file(test_data/"invalid_content.json")


#  def test_invalid(test_data):
    #  test_data1 = test_data
    #  try:
        #  with test_data1.open() as file:
            #  data = json.load(file)
        #  return data
    #  except json.decoder.JSONDecodeError:
        #  print('There is  a problem')


