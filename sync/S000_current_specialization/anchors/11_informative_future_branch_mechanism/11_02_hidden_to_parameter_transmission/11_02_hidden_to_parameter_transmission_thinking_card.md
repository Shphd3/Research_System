# Thinking Card — Hidden-to-Parameter Transmission Anchor

> Migrated from [11_02_hidden_to_parameter_transmission_anchor.md](11_02_hidden_to_parameter_transmission_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** A loss can point in a useful hidden-state direction without trainable shared parameters being able to realize that movement.

**Mechanism guess:** The task direction must survive multiplication by the hidden-state Jacobian. Other language-model losses add signed background terms that may help or cancel it.

**Observable metric:** parameter semantic velocity, the predicted change of the task margin under one shared-parameter update.

**Decision:** the parameter-transmission prerequisite is supported under the controlled interventions; its sign is not universally positive under full all-position training.
