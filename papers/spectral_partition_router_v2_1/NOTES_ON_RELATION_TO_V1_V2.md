# Relation to V1 and V2

## V1

V1 solved a strong clean case:

```text
spherical feature directions + equal-measure prototype cells -> uniform top-1 usage
```

## V2

V2 constructed equal-mass feature dispatch using recursive quantile routing:

```text
unlabeled spectrally normalized features -> equal-probability cells
```

## V2.1

V2.1 asks for a stronger router:

```text
equal-probability cells + feature coherence + margin-based preservation
```

It does not discard V2. It uses V2's quantile mass control as the first layer, then adds geometry and preservation requirements.
