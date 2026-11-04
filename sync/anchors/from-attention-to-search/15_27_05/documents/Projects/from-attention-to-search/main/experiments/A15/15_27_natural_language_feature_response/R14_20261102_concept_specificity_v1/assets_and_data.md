派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/assets_and_data.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/assets_and_data.md)；研究修改仍回到原件。

---

# R14 assets and dataset identity

Model: official Qwen3-0.6B-Base, hashcd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba; tokenizer/config hashes in manifest. A22 dictionary hash09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628;14joint blocks1,3,...,27 and16384shared coefficients. Last raw layer contribution uses checkpoint TRAIN vector RMS and mean, frozen threshold. CPU inference adaptation and native identity qualification are in amendmentsA9 and Detailed; no alternative checkpoint/model.

[All288prefixes, complete candidates, token IDs and labels](../../../../../../../../UNAVAILABLE.md) are a selected small input manifest, not an activation payload. This view corrects a deprecated length-diagnostic field only; exact actual input tokens and candidate arrays match immutable execution data/prefixes.jsonl. The original hash and erratum are recorded.48families:16/domain,4development+12evaluation each;36independent evaluation units. Family pairs have upperU,wrong upperV,siblingsA/B,broad/A/B cue prefixes and2paraphrases. Names/labels came from model-independent authored definitions, not model correctness. AIreview and reliable reference links are provided; no human blind annotation is claimed. Literal U/V/A/B exposure is absent after data1.3 repair.

Reference spectrum: R04math30/bio30documents x160positions=9600vectors,1024numerical rank, entropy effective rank281.915; reference mean/PCA reused, no new fit and no physics reference documents. Feature reference is65536DCLMpositions with recovered frozen bins; original document mapUnknown. Output-token frequency is a separate4194304token DCLMreference with inherited tokenization-revision limitation. Neither frequency is semantic granularity or Qwen exposure.

Raw caches, checkpoints and large full distributions stay in execution, with stable paths/hashes in [manifest](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/manifest.json) and [reproduction](reproduce.md). [Conditions](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/evidence/conditions.json), [families](../../../../../../../../UNAVAILABLE.md), [source audit](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/provenance/source_audit_final.json), [review](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/provenance/semantic_review_48families.json) and [coverage](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/coverage.csv) are repository-side reading evidence. Copying them does not grant new execution or scientific approval.

## All48families and exact descriptions

The two fixed wrappers are `Identify the scientific concept from the description. / Description: ... / Answer:` and `Name the concept that best fits this account. / Account: ... / Answer:` with actual newlines as in the input manifest. Broad description content is shared between wrappers; the A/B cue descriptions are genuinely paraphrased. These are not independent templates or independent families.

### biology_01 (development)

U=organelle;V=tissue;A=mitochondrion;B=Golgi apparatus.

- wording1, broad: A structure inside a eukaryotic cell performs a specialized task.

- wording1, A: This cellular structure uses an inner membrane proton gradient to make ATP during aerobic respiration.

- wording1, B: This cellular structure modifies and sorts newly made proteins into vesicles for delivery.

- wording2, broad: A structure inside a eukaryotic cell performs a specialized task.

- wording2, A: Inside this structure, oxidative phosphorylation couples electron transport to ATP production.

- wording2, B: Stacks of flattened membrane sacs receive proteins and package them for transport to other destinations.

### biology_02 (development)

U=nucleic acid;V=lipid;A=DNA;B=RNA.

- wording1, broad: A biological polymer carries information through a sequence of nucleotides.

- wording1, A: This polymer normally stores hereditary information in a double helix and contains thymine.

- wording1, B: This polymer contains uracil and can carry a copied genetic message to a ribosome.

- wording2, broad: A biological polymer carries information through a sequence of nucleotides.

- wording2, A: Its paired strands use deoxyribose sugars and preserve the genome for inheritance.

- wording2, B: Its ribose-containing strand can act as a messenger during protein synthesis.

### biology_03 (development)

U=cell division;V=digestion;A=mitosis;B=meiosis.

- wording1, broad: A eukaryotic cell separates genetic material into daughter cells.

- wording1, A: One division produces two daughter cells with the same chromosome number as the parent.

- wording1, B: Two successive divisions produce haploid products from a diploid starting cell.

- wording2, broad: A eukaryotic cell separates genetic material into daughter cells.

- wording2, A: Replicated chromosomes separate so that two genetically similar diploid daughter cells form.

- wording2, B: Homologous chromosomes pair and recombine before the chromosome number is halved.

### biology_04 (development)

U=membrane transport;V=cell division;A=active transport;B=osmosis.

- wording1, broad: Substances move across a biological membrane.

- wording1, A: A membrane pump consumes ATP to move dissolved ions against their concentration gradient.

- wording1, B: Water crosses a selectively permeable membrane toward the side with more dissolved solute.

- wording2, broad: Substances move across a biological membrane.

- wording2, A: Energy drives ions from a region of lower concentration to a region of higher concentration.

- wording2, B: A membrane allows solvent water to move while excluding the dissolved molecules.

### biology_05 (evaluation)

U=cellular structure;V=animal tissue;A=ribosome;B=lysosome.

- wording1, broad: A specialized part inside a cell performs a biochemical task.

- wording1, A: This structure reads a messenger nucleotide sequence and links amino acids into a protein.

- wording1, B: This membrane-enclosed compartment uses acidic digestive enzymes to break down worn cellular material.

- wording2, broad: A specialized part inside a cell performs a biochemical task.

- wording2, A: Transfer molecules bring amino acids to this structure, where peptide bonds extend a growing chain.

- wording2, B: Damaged cell parts enter this acidic compartment and are dismantled by hydrolytic enzymes.

### biology_06 (evaluation)

U=blood cell;V=plant cell;A=erythrocyte;B=leukocyte.

- wording1, broad: A cell circulates in vertebrate blood.

- wording1, A: This mature human cell lacks a nucleus and carries oxygen using hemoglobin.

- wording1, B: This nucleated cell circulates in vertebrates and participates in defense against infectious agents.

- wording2, broad: A cell circulates in vertebrate blood.

- wording2, A: Its biconcave shape and abundant hemoglobin support oxygen delivery to tissues.

- wording2, B: It can leave small vessels and act against invading microbes as part of immune defense.

### biology_07 (evaluation)

U=blood vessel;V=digestive organ;A=artery;B=vein.

- wording1, broad: A tubular structure carries blood in the circulation.

- wording1, A: Blood in this vessel moves away from the heart under relatively high pressure.

- wording1, B: Blood in this vessel returns toward the heart, often aided by valves.

- wording2, broad: A tubular structure carries blood in the circulation.

- wording2, A: Its thick elastic wall handles blood ejected directly from a pumping heart chamber.

- wording2, B: One-way valves help this low-pressure vessel carry blood back toward the heart.

### biology_08 (evaluation)

U=plant vascular tissue;V=animal nervous tissue;A=xylem;B=phloem.

- wording1, broad: A tissue transports materials through a vascular plant.

- wording1, A: This tissue carries water and mineral ions upward through mostly dead conducting cells.

- wording1, B: This tissue transports dissolved sugars between sources and sinks through living sieve elements.

- wording2, broad: A tissue transports materials through a vascular plant.

- wording2, A: Lignified conducting tubes supply leaves with water drawn from the roots.

- wording2, B: Companion cells support living tubes that distribute the products of photosynthesis.

### biology_09 (evaluation)

U=immune cell;V=muscle cell;A=B lymphocyte;B=T lymphocyte.

- wording1, broad: A lymphocyte participates in adaptive immunity.

- wording1, A: After activation, this cell lineage can form plasma cells that secrete antibodies.

- wording1, B: This cell lineage matures in the thymus and recognizes peptide fragments presented by other cells.

- wording2, broad: A lymphocyte participates in adaptive immunity.

- wording2, A: Its descendants release soluble antibodies that bind a particular antigen.

- wording2, B: Its receptors recognize displayed peptide complexes and can direct cellular killing.

### biology_10 (evaluation)

U=ecological interaction;V=geological process;A=mutualism;B=parasitism.

- wording1, broad: Two species interact closely in an ecosystem.

- wording1, A: Both participating species receive a net benefit from their association.

- wording1, B: One participant benefits by obtaining resources while the other is harmed.

- wording2, broad: Two species interact closely in an ecosystem.

- wording2, A: Each partner gains resources or services that improve its own biological performance.

- wording2, B: A smaller organism takes nutrients from a host and reduces the host survival or reproduction.

### biology_11 (evaluation)

U=trophic role;V=reproductive organ;A=producer;B=consumer.

- wording1, broad: An organism occupies a role in the flow of energy through an ecosystem.

- wording1, A: This organism makes organic food from inorganic carbon using light or chemical energy.

- wording1, B: This organism obtains organic food by eating other organisms or their products.

- wording2, broad: An organism occupies a role in the flow of energy through an ecosystem.

- wording2, A: It fixes carbon into biomass and supplies the entry point for energy into a food web.

- wording2, B: It depends on pre-existing organic matter rather than fixing its own carbon supply.

### biology_12 (evaluation)

U=evolutionary process;V=cellular organelle;A=genetic drift;B=natural selection.

- wording1, broad: Allele frequencies change over generations in a population.

- wording1, A: Random sampling changes allele frequencies most strongly in a small population.

- wording1, B: Heritable variants become more common because their bearers leave more surviving offspring.

- wording2, broad: Allele frequencies change over generations in a population.

- wording2, A: A chance bottleneck alters the population gene pool without requiring an adaptive advantage.

- wording2, B: Variants associated with higher reproductive success systematically increase across generations.

### biology_13 (evaluation)

U=enzyme;V=carbohydrate;A=DNA polymerase;B=RNA polymerase.

- wording1, broad: A molecule accelerates the assembly of a nucleic acid strand along a template without being consumed.

- wording1, A: This molecule extends a new genome copy using deoxyribonucleotides during replication.

- wording1, B: This molecule makes a ribonucleotide transcript from a genomic template.

- wording2, broad: A molecule accelerates the assembly of a nucleic acid strand along a template without being consumed.

- wording2, A: It adds deoxyribonucleotides to the growing daughter strand during duplication of hereditary material.

- wording2, B: It initiates a transcript at a promoter and builds a messenger strand.

### biology_14 (evaluation)

U=animal tissue;V=plant organ;A=epithelial tissue;B=connective tissue.

- wording1, broad: A collection of animal cells performs a shared bodily function.

- wording1, A: Closely packed cells form a continuous sheet lining a body cavity or covering a surface.

- wording1, B: Cells are dispersed within an abundant extracellular matrix that supports and binds structures.

- wording2, broad: A collection of animal cells performs a shared bodily function.

- wording2, A: A tightly joined cellular layer creates a protective and absorptive boundary.

- wording2, B: Fibers and ground substance surrounding scattered cells provide structural support.

### biology_15 (evaluation)

U=plant reproductive process;V=circulatory process;A=fertilization;B=pollination.

- wording1, broad: An event contributes to sexual reproduction in a flowering plant.

- wording1, A: A male gamete fuses with an egg to produce a zygote.

- wording1, B: Pollen is transferred from an anther to a receptive stigma.

- wording2, broad: An event contributes to sexual reproduction in a flowering plant.

- wording2, A: Two gamete nuclei unite and establish a new diploid cell.

- wording2, B: An animal delivers pollen grains to the female receptive surface before gamete fusion.

### biology_16 (evaluation)

U=hormone;V=digestive enzyme;A=insulin;B=glucagon.

- wording1, broad: A pancreatic chemical messenger regulates blood glucose.

- wording1, A: This messenger is released by beta cells and promotes glucose uptake when blood sugar is high.

- wording1, B: This messenger is released by alpha cells and promotes glucose release when blood sugar is low.

- wording2, broad: A pancreatic chemical messenger regulates blood glucose.

- wording2, A: After a meal, it encourages storage of glucose as glycogen and lowers circulating glucose.

- wording2, B: During fasting, it stimulates breakdown of liver glycogen and raises circulating glucose.

### mathematics_01 (development)

U=calculus operation;V=geometric shape;A=differentiation;B=integration.

- wording1, broad: A mathematical operation is applied to a real-valued function.

- wording1, A: The operation finds the instantaneous rate of change by taking a limit of difference quotients.

- wording1, B: The operation accumulates infinitesimal contributions to find signed area over an interval.

- wording2, broad: A mathematical operation is applied to a real-valued function.

- wording2, A: It assigns the tangent slope at each point where that slope exists.

- wording2, B: It sums contributions across a continuous interval rather than evaluating a pointwise slope.

### mathematics_02 (development)

U=triangle;V=quadrilateral;A=equilateral triangle;B=right triangle.

- wording1, broad: A polygon has three sides.

- wording1, A: All three sides have the same length, so each interior angle is sixty degrees.

- wording1, B: One interior angle is ninety degrees.

- wording2, broad: A polygon has three sides.

- wording2, A: Its three equal side lengths force three equal interior angles.

- wording2, B: Two sides meet perpendicularly, and the opposite side is the hypotenuse.

### mathematics_03 (development)

U=event relation;V=number system;A=independence;B=mutual exclusivity.

- wording1, broad: Two events have a specified relation in a probability experiment.

- wording1, A: Knowing that the first event occurred does not change the probability of the second.

- wording1, B: Both events have positive probability, but they cannot occur on the same trial.

- wording2, broad: Two events have a specified relation in a probability experiment.

- wording2, A: The probability of their intersection equals the product of their probabilities.

- wording2, B: Their intersection is empty even though each event can occur on its own.

### mathematics_04 (development)

U=average;V=geometric transformation;A=arithmetic mean;B=geometric mean.

- wording1, broad: A single number summarizes a list of positive measurements.

- wording1, A: Add all observations and divide by the number of observations.

- wording1, B: Multiply all observations and take the root whose order is the number of observations.

- wording2, broad: A single number summarizes a list of positive measurements.

- wording2, A: The total of the measurements is shared equally among all entries.

- wording2, B: The summary preserves their product when every entry is replaced by the same value.

### mathematics_05 (evaluation)

U=conic section;V=probability distribution;A=ellipse;B=hyperbola.

- wording1, broad: A curve is obtained by intersecting a plane with a cone.

- wording1, A: For every point on this closed curve, the sum of distances to two fixed foci is constant.

- wording1, B: For every point on this two-branched curve, the absolute difference of distances to two foci is constant.

- wording2, broad: A curve is obtained by intersecting a plane with a cone.

- wording2, A: Its points surround two foci while maintaining a fixed total distance from them.

- wording2, B: Its two disconnected branches approach straight asymptotes and maintain a fixed focal distance difference.

### mathematics_06 (evaluation)

U=function;V=geometric solid;A=exponential function;B=logarithmic function.

- wording1, broad: An input value is assigned exactly one output value according to a fixed mathematical rule.

- wording1, A: The input occurs in the exponent of a fixed positive base other than one.

- wording1, B: The output gives the exponent required for a fixed base to produce the positive input.

- wording2, broad: An input value is assigned exactly one output value according to a fixed mathematical rule.

- wording2, A: Equal increments in the input multiply the output by the same positive factor.

- wording2, B: It is the inverse of raising a fixed positive base to a variable power.

### mathematics_07 (evaluation)

U=sequence;V=plane curve;A=arithmetic sequence;B=geometric sequence.

- wording1, broad: A list of numbers follows a fixed recursive rule.

- wording1, A: Subtracting each term from the next gives the same nonzero constant.

- wording1, B: Dividing each term by the previous nonzero term gives the same ratio, distinct from one.

- wording2, broad: A list of numbers follows a fixed recursive rule.

- wording2, A: Each new term is obtained by adding a fixed nonzero increment to its predecessor.

- wording2, B: Each new term is obtained by multiplying its predecessor by a fixed factor.

### mathematics_08 (evaluation)

U=real number;V=matrix;A=rational number;B=irrational number.

- wording1, broad: A numerical quantity can be located as a point on a continuous number line.

- wording1, A: The number can be expressed as a ratio of two integers with a nonzero denominator.

- wording1, B: The number cannot be expressed as a ratio of integers and has a nonrepeating infinite decimal expansion.

- wording2, broad: A numerical quantity can be located as a point on a continuous number line.

- wording2, A: Its decimal expansion either terminates or eventually repeats a finite block.

- wording2, B: Its decimal expansion neither terminates nor settles into a repeating block.

### mathematics_09 (evaluation)

U=matrix;V=scalar;A=symmetric matrix;B=skew-symmetric matrix.

- wording1, broad: A real square array is compared with its transpose.

- wording1, A: Transposing the array leaves it unchanged, and at least one off-diagonal entry is nonzero.

- wording1, B: Transposing the array gives its negative, and at least one entry is nonzero.

- wording2, broad: A real square array is compared with its transpose.

- wording2, A: Entries on opposite sides of the main diagonal are equal, with at least one nonzero pair.

- wording2, B: Entries on opposite sides of the diagonal have opposite signs, and every diagonal entry is zero.

### mathematics_10 (evaluation)

U=mapping;V=polynomial;A=injection;B=surjection.

- wording1, broad: A function maps elements from one set into another set.

- wording1, A: Different inputs always give different outputs, but at least one codomain element is not reached.

- wording1, B: Every codomain element is reached, but two distinct inputs have the same output.

- wording2, broad: A function maps elements from one set into another set.

- wording2, A: No output has more than one preimage, although the codomain includes an unused element.

- wording2, B: The image equals the codomain even though some output has multiple preimages.

### mathematics_11 (evaluation)

U=local extremum;V=linear equation;A=local maximum;B=local minimum.

- wording1, broad: A smooth function has an interior critical point.

- wording1, A: Nearby function values on both sides are strictly lower than the value at this point.

- wording1, B: Nearby function values on both sides are strictly higher than the value at this point.

- wording2, broad: A smooth function has an interior critical point.

- wording2, A: The curve rises toward the point from the left and falls away on the right.

- wording2, B: The curve falls toward the point from the left and rises away on the right.

### mathematics_12 (evaluation)

U=infinite series;V=finite polygon;A=convergent series;B=divergent series.

- wording1, broad: Infinitely many terms are added through a sequence of partial sums.

- wording1, A: The partial sums approach a finite limit as the number of terms grows without bound.

- wording1, B: The partial sums do not approach any finite limit as the number of terms grows without bound.

- wording2, broad: Infinitely many terms are added through a sequence of partial sums.

- wording2, A: Successive partial sums settle arbitrarily close to one finite value.

- wording2, B: The sequence of partial sums fails to settle to a finite value.

### mathematics_13 (evaluation)

U=vector operation;V=probability event;A=dot product;B=cross product.

- wording1, broad: An operation combines two vectors in three-dimensional space.

- wording1, A: Its scalar output equals the product of the vector magnitudes and the cosine of their angle.

- wording1, B: Its vector output is perpendicular to both inputs, with orientation set by the right-hand rule.

- wording2, broad: An operation combines two vectors in three-dimensional space.

- wording2, A: Multiply corresponding components and add the resulting numbers to obtain one scalar.

- wording2, B: The output magnitude is the parallelogram area and its direction is normal to the input plane.

### mathematics_14 (evaluation)

U=positive integer;V=continuous function;A=prime number;B=composite number.

- wording1, broad: An integer greater than one is classified by its divisors.

- wording1, A: Its only positive divisors are one and the integer itself.

- wording1, B: It has a positive divisor other than one and itself.

- wording2, broad: An integer greater than one is classified by its divisors.

- wording2, A: It cannot be written as a product of two smaller integers greater than one.

- wording2, B: It can be factored into two integers that are both greater than one.

### mathematics_15 (evaluation)

U=plane isometry;V=random variable;A=rotation;B=reflection.

- wording1, broad: A transformation of the plane preserves distances.

- wording1, A: Every point turns through a fixed angle around a fixed center, preserving orientation.

- wording1, B: Points are sent to their mirror images across a fixed line, reversing orientation.

- wording2, broad: A transformation of the plane preserves distances.

- wording2, A: A center stays fixed while all other points move through the same signed angle.

- wording2, B: Each point and its image lie equally far from a line on opposite sides.

### mathematics_16 (evaluation)

U=polynomial;V=trigonometric function;A=linear polynomial;B=quadratic polynomial.

- wording1, broad: A nonconstant expression in one variable is a finite sum of terms whose powers are nonnegative integers.

- wording1, A: Its highest nonzero power of the variable is one.

- wording1, B: Its highest nonzero power of the variable is two.

- wording2, broad: A nonconstant expression in one variable is a finite sum of terms whose powers are nonnegative integers.

- wording2, A: Its graph is a straight line with a nonzero slope.

- wording2, B: Its graph is a parabola because the squared-variable coefficient is nonzero.

### physics_01 (development)

U=wave phenomenon;V=chemical reaction;A=reflection;B=refraction.

- wording1, broad: A light ray changes direction at a boundary.

- wording1, A: The ray returns into the original medium with its outgoing angle equal to the incident angle.

- wording1, B: The ray enters a second medium and bends because its propagation speed changes.

- wording2, broad: A light ray changes direction at a boundary.

- wording2, A: The light bounces back from the surface rather than crossing into another material.

- wording2, B: The transmitted beam changes its direction when it crosses between media with different optical densities.

### physics_02 (development)

U=kinematic quantity;V=electrical quantity;A=velocity;B=acceleration.

- wording1, broad: A vector quantity describes the motion of a particle.

- wording1, A: This quantity is the time derivative of position.

- wording1, B: This quantity is the time derivative of the rate of change of position.

- wording2, broad: A vector quantity describes the motion of a particle.

- wording2, A: Divide a small displacement by the corresponding time interval and take the instantaneous limit.

- wording2, B: Track how the motion vector changes per unit time, including changes of direction.

### physics_03 (development)

U=energy;V=electric charge;A=kinetic energy;B=potential energy.

- wording1, broad: A physical system has a measurable capacity to do work.

- wording1, A: For a slowly moving massive particle, this quantity is one half its mass times speed squared.

- wording1, B: This quantity is stored because of position or configuration in a conservative force field.

- wording2, broad: A physical system has a measurable capacity to do work.

- wording2, A: Bringing a moving object to rest removes this motion-dependent quantity.

- wording2, B: Raising an object in a gravitational field increases this configuration-dependent quantity.

### physics_04 (development)

U=electrical component;V=optical component;A=resistor;B=capacitor.

- wording1, broad: An element is connected into an electrical circuit.

- wording1, A: This element dissipates energy as heat and relates voltage to current by a resistance.

- wording1, B: This element stores energy in an electric field between separated conducting surfaces.

- wording2, broad: An element is connected into an electrical circuit.

- wording2, A: A steady current through the element produces a voltage drop and thermal heating.

- wording2, B: Opposite charges accumulate on two plates separated by an insulating gap.

### physics_05 (evaluation)

U=force;V=temperature;A=friction;B=buoyancy.

- wording1, broad: An interaction pushes or pulls on an object and can change its motion.

- wording1, A: At a sliding contact, this tangential interaction opposes relative motion of the surfaces.

- wording1, B: A pressure difference in a fluid produces an upward push equal to the weight of the displaced fluid.

- wording2, broad: An interaction pushes or pulls on an object and can change its motion.

- wording2, A: Two solid surfaces rub, producing a tangential resistance to sliding.

- wording2, B: An immersed object experiences a net upward push because fluid pressure is greater at its bottom.

### physics_06 (evaluation)

U=heat transfer;V=electric charging;A=conduction;B=convection.

- wording1, broad: Thermal energy moves from a warmer region to a cooler region.

- wording1, A: Energy crosses a stationary solid through microscopic interactions without bulk material flow.

- wording1, B: Energy is carried by the bulk circulation of warmer and cooler fluid.

- wording2, broad: Thermal energy moves from a warmer region to a cooler region.

- wording2, A: A metal bar transports thermal energy along its length while its material remains in place.

- wording2, B: Rising warm liquid and sinking cool liquid carry thermal energy through a container.

### physics_07 (evaluation)

U=thermodynamic process;V=optical phenomenon;A=isothermal process;B=adiabatic process.

- wording1, broad: A gas undergoes a controlled change of state.

- wording1, A: The gas changes volume while its temperature stays constant through heat exchange.

- wording1, B: The gas changes volume without exchanging heat with its surroundings.

- wording2, broad: A gas undergoes a controlled change of state.

- wording2, A: A heat reservoir keeps the gas temperature fixed during a slow expansion.

- wording2, B: Thermal insulation prevents heat from crossing the boundary during compression.

### physics_08 (evaluation)

U=electromagnetic radiation;V=sound wave;A=infrared radiation;B=ultraviolet radiation.

- wording1, broad: Radiation occupies a band next to visible light in the electromagnetic spectrum.

- wording1, A: Its wavelength is longer than visible red light, and warm objects emit it strongly.

- wording1, B: Its wavelength is shorter than visible violet light, and it can cause sunburn.

- wording2, broad: Radiation occupies a band next to visible light in the electromagnetic spectrum.

- wording2, A: Thermal imaging detects this band on the long-wavelength side of the visible spectrum.

- wording2, B: This band beyond the short-wavelength edge of visible light can damage exposed skin.

### physics_09 (evaluation)

U=atomic process;V=fluid motion;A=absorption;B=emission.

- wording1, broad: An atom exchanges a photon with its surroundings.

- wording1, A: The atom takes in a photon and moves to a higher allowed energy level.

- wording1, B: The atom releases a photon and moves to a lower allowed energy level.

- wording2, broad: An atom exchanges a photon with its surroundings.

- wording2, A: Incoming light supplies exactly the energy gap needed to excite the atom.

- wording2, B: A downward transition produces an outgoing photon whose energy equals the level difference.

### physics_10 (evaluation)

U=oscillation;V=static equilibrium;A=damped oscillation;B=driven oscillation.

- wording1, broad: A mechanical system repeatedly moves around an equilibrium position.

- wording1, A: After an initial displacement without any subsequent applied force, resistance gradually reduces its amplitude.

- wording1, B: A continuing periodic external force maintains the repeated motion against losses.

- wording2, broad: A mechanical system repeatedly moves around an equilibrium position.

- wording2, A: The freely moving system loses mechanical energy and its successive peaks shrink.

- wording2, B: An outside actuator supplies a repeating force that sustains the motion over many cycles.

### physics_11 (evaluation)

U=mechanical wave;V=static field;A=transverse wave;B=longitudinal wave.

- wording1, broad: A disturbance propagates through a material medium.

- wording1, A: Particles of the medium move perpendicular to the direction of propagation.

- wording1, B: Particles of the medium move parallel to the direction of propagation.

- wording2, broad: A disturbance propagates through a material medium.

- wording2, A: A pulse travels along a stretched string while the string moves up and down.

- wording2, B: Alternating compressions and rarefactions travel while the medium vibrates along the travel direction.

### physics_12 (evaluation)

U=lens;V=electric circuit;A=converging lens;B=diverging lens.

- wording1, broad: A transparent optical element changes the paths of light rays.

- wording1, A: Initially parallel rays emerge heading toward a common real focal point.

- wording1, B: Initially parallel rays spread apart as though they originated at a virtual focal point.

- wording2, broad: A transparent optical element changes the paths of light rays.

- wording2, A: The element brings an incoming parallel beam together on the opposite side.

- wording2, B: The element makes an incoming parallel beam fan outward after transmission.

### physics_13 (evaluation)

U=circuit connection;V=wave polarization;A=series connection;B=parallel connection.

- wording1, broad: Two resistive components are joined in an electrical network.

- wording1, A: There is only one current path, so the same current passes through both components.

- wording1, B: Both components connect across the same two nodes, so they share a voltage.

- wording2, broad: Two resistive components are joined in an electrical network.

- wording2, A: Charges must pass through the first component and then through the second with no branching path.

- wording2, B: Current can divide between two branches that start and end at the same pair of nodes.

### physics_14 (evaluation)

U=magnetic material;V=electric field;A=ferromagnetic material;B=diamagnetic material.

- wording1, broad: A sample responds to an applied magnetic field.

- wording1, A: Aligned magnetic domains can produce strong magnetization that persists after the field is removed.

- wording1, B: An induced weak magnetization opposes the applied field and vanishes when it is removed.

- wording2, broad: A sample responds to an applied magnetic field.

- wording2, A: The sample can retain a strong remanent magnetic moment because many domains align.

- wording2, B: The sample is weakly repelled from regions of stronger field through an opposing induced response.

### physics_15 (evaluation)

U=subatomic particle;V=molecule;A=electron;B=proton.

- wording1, broad: A charged constituent of an ordinary atom is described.

- wording1, A: This light particle has negative elementary charge and occupies states outside the nucleus.

- wording1, B: This heavier particle has positive elementary charge and is a constituent of the nucleus.

- wording2, broad: A charged constituent of an ordinary atom is described.

- wording2, A: It carries one negative unit of charge and has much less mass than a nucleon.

- wording2, B: It carries one positive unit of charge and helps determine the atomic number.

### physics_16 (evaluation)

U=mechanical quantity;V=thermodynamic quantity;A=momentum;B=torque.

- wording1, broad: A vector quantity is used in describing mechanical motion.

- wording1, A: For a nonrelativistic particle, it equals mass times the translational motion vector.

- wording1, B: It equals the cross product of a lever-arm vector and an applied force.

- wording2, broad: A vector quantity is used in describing mechanical motion.

- wording2, A: The quantity is conserved for an isolated system and changes under a net force impulse.

- wording2, B: This turning effect depends on both the applied force and its perpendicular distance from the pivot.
