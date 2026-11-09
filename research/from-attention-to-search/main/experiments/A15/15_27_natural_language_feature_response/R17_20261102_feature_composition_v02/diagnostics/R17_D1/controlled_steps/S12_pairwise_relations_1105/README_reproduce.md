# Replay S12

Python3,numpy,scipy,pandas,scikit-learn,matplotlib;g++forCurveball. No model/SAE weights or forward required. All primary cache inputs are reusedS11; paths/hashes in evidence/input_manifest.json.

`python code/verify.py` independently recomputes counts,logOR,coverage,readoutloss,640full-margin snapshots and S11 input immutability on the original host. A portable packet includes primarysplitCSRfiles under inputs/; use `python code/portable_replay.py` for model-free edge/readout/fullmargin replay without original paths.

Analysis order (do not overwrite original frozen receipts):copy packet to new output root;point S11 in common.py to originalS11;prepare.py -> freezeprotocol -> select_development.py -> evaluate.py -> readouts.py -> extra_exports.py -> figures.py -> verify.py -> write_reports.py. prepare/select refuse existing freeze/lock. Full null traces and states are included if listed in package manifest; compiled .so is excluded and recompiles from source. Existing selection.json is the actual locked list,not a new selection. Reexecuting evaluation is not a fresh confirmation.

CSV count arrays are JSON strings ordered[n11,n10,n01,n00]. logOR unit:natural logarithm; strengthcontrast:Fisherz; classifierloss:nat/text,pairedfamilymean. Draw seeds/formulas/eligibility and unadjusted auxiliary comparisons are explicit in protocol.md.

Figures:PNGforreading,SVGeditable. Fonts are external originalsystemassets,not packaged;use an available CJK font for rerendering. Sourceaudit optionalpypdfreader does not affect analysis.

Inputreferencefulltexts/modelweights/bodyactivations are not copied. NodeQ/Gcounts/N are preserved;fullreferencefrequencies remain at S11 and have inputhashes. No claim that this packet is a new independent dataset.
