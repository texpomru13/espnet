#!/usr/bin/env python3

# Copyright 2018 Nagoya University (Tomoki Hayashi)
#  Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

import argparse
import codecs
import nltk
import collections

#from text.cleaners import custom_english_cleaners
from text import text_to_sequence, cmudict
cmd = cmudict.CMUDict('local/rudic.pcl')


# try:
#     clean_text = _clean_text(text, cleaner_names)
#     # For phoneme conversion, use https://github.com/Kyubyong/g2p.
#     from g2p_en import G2p
#     f_g2p = G2p()
#     f_g2p("")
# except ImportError:
#     raise ImportError("g2p_en is not installed. please run `. ./path.sh && pip install g2p_en`.")
# except LookupError:
#     # NOTE: we need to download dict in initial running
#     nltk.download("punkt")


def g2p(text):
    """Convert grapheme to phoneme."""
    tokens = filter(lambda s: s != " ", f_g2p(text))
    return ' '.join(tokens)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('text', type=str, help='text to be cleaned')
    parser.add_argument("trans_type", type=str, default="kana",
                        choices=["char", "phn"],
                        help="Input transcription type")
    args = parser.parse_args()
    with codecs.open(args.text, 'r', 'utf-8') as fid:
        dct = {}
        for line in fid.readlines():
            id, content = line.split("|")
            dct[id] = content.rstrip()

        od = collections.OrderedDict(sorted(dct.items()))
        #clean_content = custom_english_cleaners(content.rstrip())
        for id in od:
            if args.trans_type == "phn":    
                # text = clean_content.lower()
                # clean_content = g2p(text)
                _, clean_content = text_to_sequence(od[id], ['basic_cleaners'], cmd)

            print("%s %s" % (id, clean_content))
