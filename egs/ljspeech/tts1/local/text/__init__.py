""" from https://github.com/keithito/tacotron """
import re
from text import cleaners
from text.symbols import symbols


# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}

# Regular expression matching text enclosed in curly braces:
_curly_re = re.compile(r'(.*?)\{(.+?)\}(.*)')

val_sybols = 'йцукенгшщзхъёфывапролджэячсмитьбю-'
punctuation = '!\'"(),.:;…? '


def get_arpabet(word, dictionary):
#   if word[-1] in punctuation:
#     word_arpabet = dictionary.lookup(word[:-1])
#   elif word[0] in punctuation and word[-1] in punctuation:
#     word_arpabet = dictionary.lookup(word[1:-1])
#   else:
  if word in punctuation:
    return word
  word_arpabet = dictionary.lookup(word)
  if word_arpabet is not None:
    return "{" + word_arpabet + "}"
  else:
    return word


def text_to_sequence(text, cleaner_names, dictionary=None):
  '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.

    The text can optionally have ARPAbet sequences enclosed in curly braces embedded
    in it. For example, "Turn left on {HH AW1 S S T AH0 N} Street."

    Args:
      text: string to convert to a sequence
      cleaner_names: names of the cleaner functions to run the text through
      dictionary: arpabet class with arpabet dictionary

    Returns:
      List of integers corresponding to the symbols in the text
  '''
  sequence = []

  space = _symbols_to_sequence(' ')
  # Check for curly braces and treat their contents as ARPAbet:
  #print(text)
  while len(text):
    m = _curly_re.match(text)
    if not m:
      clean_text = _clean_text(text, cleaner_names)
      #print(clean_text)
      if cmudict is not None:
        #print('cmudict')
        #print(clean_text.split(" "))
        n_clean_text = ''
        
        for wo in clean_text.split(" "):
          word = ''
          for j in wo:
            if j in val_sybols:
              word += j

            elif j in punctuation:
              if word == "" and j == '"':
                word += '" '
              elif j == '(':
                word += '( '
              else:
                word += " "+j
              
          if n_clean_text == "":
            n_clean_text += word
          else:
            n_clean_text += " "+word
          

        #print(n_clean_text)
        n_clean_text = [get_arpabet(w, dictionary) for w in n_clean_text.split(" ")]
        clean_text = []
        for i in n_clean_text:
          if i != '':
            clean_text.append(i)
        #print(clean_text)
        for i in range(len(clean_text)):
            t = clean_text[i]
            #is_punkt
            if t in punctuation:
              try:
                sequence.pop()
              except:
                # print(clean_text)
            if t.startswith("{"):
              sequence += _arpabet_to_sequence(t[1:-1])
            else:
              sequence +=  _symbols_to_sequence(t)
            sequence += space
      else:
        sequence += _symbols_to_sequence(clean_text)
      break

    clean_text = _clean_text(text, cleaner_names)
    sequence += _symbols_to_sequence(_clean_text(m.group(1), cleaner_names))
    sequence += _arpabet_to_sequence(m.group(2))
    text = m.group(3)

  # remove trailing space
  sequence = sequence[:-1] if sequence[-1] == space[0] else sequence
  #sequence = sequence[1:]
  sequence.append(_symbol_to_id['~'])
  prep_txt = []
  spaceadd = False
  for i in clean_text:
    addtxt = ''
    
    if i.startswith("{"):
      addtxt = i[1:-1]
    else:
      addtxt = i
      spaceadd = False

    if spaceadd:
      prep_txt.append('<space>')
      prep_txt.append(addtxt)
    else:
      prep_txt.append(addtxt)
      spaceadd = True
  prep_txt.append('<eos>')



  #print(sequence)
  return sequence, ' '.join(prep_txt)


def sequence_to_text(sequence):
  '''Converts a sequence of IDs back to a string'''
  result = ''
  for symbol_id in sequence:
    if symbol_id in _id_to_symbol:
      s = _id_to_symbol[symbol_id]
      # Enclose ARPAbet back in curly braces:
      if len(s) > 1 and s[0] == '@':
        s = '{%s}' % s[1:]
      result += s
  return result.replace('}{', ' ')


def _clean_text(text, cleaner_names):
  for name in cleaner_names:
    cleaner = getattr(cleaners, name)
    if not cleaner:
      raise Exception('Unknown cleaner: %s' % name)
    text = cleaner(text)
  return text


def _symbols_to_sequence(symbols):
  return [_symbol_to_id[s] for s in symbols if _should_keep_symbol(s)]


def _arpabet_to_sequence(text):
  return _symbols_to_sequence(['@' + s for s in text.split()])


def _should_keep_symbol(s):
  return s in _symbol_to_id and s is not '_' and s is not '~'

