# execution_dictionary_cost

AI分析；研究者判断Unknown。Dictionary encoder parameters are additional frozen inference compute/storage. Decoder is loaded only for reconstruction diagnostics, not needed for route selection. Main trainable architecture count alone does not describe total inference footprint.

| arm   |   main_model_parameters |   additional_frozen_encoder_parameters |   additional_diagnostic_decoder_parameters |   encoding_layers | gate     | teacher_inference   |
|:------|------------------------:|---------------------------------------:|-------------------------------------------:|------------------:|:---------|:--------------------|
| A9    |               507988992 |                               67174400 |                                   67108864 |                 8 | fixed0.5 | False               |
| A9d   |               507988992 |                               33587200 |                                   33554432 |                 4 | fixed0.5 | False               |
