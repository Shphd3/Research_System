# A15_01_04 Thinking Card: Can Progressive Band Routing Form Useful Experts?

- **Current judgment:** the absence of a stable layer--band hierarchy in existing models may reflect the fact that they were never explicitly trained to dispatch successive depths through different bands. Assigning head, middle, and tail to blocks 2, 3, and 4 may create a different learning path.
- **Mechanism:** a linear Gate learns high-variance directions first. Prescribing a band by depth may expose successive experts to different token conditions; relaying every band from block 1 may additionally provide a more stable cross-layer coordinate than each layer's evolving local spectrum.
- **Strongest rival:** fixed H/M/T views merely discard information or impose an arbitrary bottleneck. They may change routes without improving expert utility, update compatibility, or language-model loss; apparent effects may instead come from load, compute, or stochastic continuation.
- **Evidence that changes the judgment:** from the same early checkpoint, data cursor, optimizer, parameter count, and load rule, two paired continuations show lower 2B held-out NLL for a progressive arm and a concordant improvement in an independent expert-function measure.
- **Next decision:** compare native, local-HMT, and layer1-relay-HMT; close fixed progressive bands as a Router design if they only redistribute tokens.

