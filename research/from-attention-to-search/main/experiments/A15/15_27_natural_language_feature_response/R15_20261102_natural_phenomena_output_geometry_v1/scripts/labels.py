"""Prefix-only descriptive candidates; no activation, feature or PC input."""
import re
FLAGS={
'negation':('近期否定词',r'\b(?:not|no|never|neither|nor|without|cannot|can.t|doesn.t|isn.t|wasn.t)\b',160),
'comparison':('近期比较标记',r'\b(?:than|versus|compared|whereas|unlike|rather than|in contrast)\b',200),
'definition':('定义或命名短语',r'\b(?:is defined as|are defined as|refers to|refer to|is called|are called|known as|means that)\b',240),
'quantity':('近期数字表达',r'\d',120),
'citation':('括号或引注片段',r'\[[^\]]{0,50}\]|\([^)]{0,70}\)',180),
'quotation':('近期引号',r'["“”]',160),
'list_marker':('可见行的列表标记',r'(?:^|\n)\s*(?:[-*•]|\d+[.)])\s',200),
'math_notation':('公式符号或排版',r'[=<>∑∫∀∈]|\\(?:frac|begin|end|alpha|beta|sum|int)|\$[^$]{0,80}\$',180),
'first_person':('近期第一人称',r'\b(?:I|we|my|our|us)\b',160),
'bio_terms':('近期生物词面',r'\b(?:cell|cells|protein|gene|genes|DNA|RNA|species|enzyme|bacteria|genome)\b',180),
'math_terms':('近期数学词面',r'\b(?:theorem|lemma|algebra|integral|equation|matrix|polynomial|integer|proof|function)\b',180),
'physics_terms':('近期物理词面',r'\b(?:quantum|electron|photon|magnetic|gravity|velocity|wavelength|particle|energy|force)\b',180),
}
NAMES={k:v[0] for k,v in FLAGS.items()};NAMES.update({'current_punctuation':'当前位置为标点片段','current_number':'当前位置为数字片段','current_format':'当前位置为空白片段'})
def label(row):
 text=row['visible_prefix'];out={k:bool(re.search(pattern,text[-window:],re.I if k!='first_person' else 0)) for k,(_,pattern,window) in FLAGS.items()}
 out.update({'current_punctuation':row['token_category']=='punctuation','current_number':row['token_category']=='number','current_format':row['token_category']=='format'})
 return out
