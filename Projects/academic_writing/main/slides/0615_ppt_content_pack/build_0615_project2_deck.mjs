import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

const ROOT = "C:\\Users\\250010109\\data\\Research_System";
const PACK = path.join(ROOT, "Projects", "academic_writing", "main", "slides", "0615_ppt_content_pack");
const FIG = path.join(PACK, "figures");
const OUT = path.join(PACK, "pptx_output");
const WORKSPACE = "C:\\Users\\250010109\\AppData\\Local\\Temp\\codex-presentations\\academic_writing_0615_build";
const SKILL_DIR =
  process.env.SKILL_DIR ||
  "C:\\Users\\250010109\\.codex\\plugins\\cache\\openai-primary-runtime\\presentations\\26.614.11602\\skills\\presentations";

async function loadArtifactTool() {
  const utilsPath = path.join(SKILL_DIR, "scripts", "artifact_tool_utils.mjs");
  const utils = await import(pathToFileURL(utilsPath).href);
  await utils.ensureArtifactToolWorkspace(WORKSPACE);
  return {
    ...(await utils.importArtifactTool(WORKSPACE)),
    readImageBlob: utils.readImageBlob,
    saveBlobToFile: utils.saveBlobToFile,
  };
}

const W = 1280;
const H = 720;
const page = { left: 76, top: 68, width: 1128, height: 584 };
const font = "HarmonyOS Sans";
const c = {
  magenta: "#881E55",
  magentaDark: "#5E173E",
  blue: "#29AAE3",
  pink: "#D14AA4",
  yellow: "#FBB900",
  ink: "#17141A",
  muted: "#5B5960",
  light: "#F6F4F7",
  line: "#E5E1E8",
  white: "#FFFFFF",
  green: "#0E7A63",
  red: "#B42318",
};

const slides = [
  {
    no: "01",
    title: "Why Sparse MoE Routers Collapse Before They Specialize",
    kicker: "Academic Writing Project 2 | 12-min research update",
    subtitle: "An audit of expert-spectrum initialization and early routing amplification",
    kind: "title",
    image: "s02_background_gap_diagram.png",
    notes:
      "Today I will present a mechanism audit of sparse mixture-of-experts routing. The main question is not whether I already have a complete new routing method. The question is why a top-1 MoE router can concentrate many tokens onto a few experts before useful specialization has time to form. The latest result tests one natural initialization idea and shows that the story is more dynamic than initialization alone.",
  },
  {
    no: "02",
    title: "MoE scaling is router-limited, not only expert-limited",
    bullets: [
      "Sparse MoE activates only a few experts per token; the router controls data and gradient flow.",
      "Load imbalance can leave many experts under-trained even in a large model.",
      "Recent work suggests router decisions often reflect hidden-state geometry rather than clean domain expertise.",
    ],
    image: "s02_background_gap_diagram.png",
    caption: "Literature boundary: routing geometry is meaningful, but not automatically semantic specialization.",
    notes:
      "A sparse MoE model increases parameter count by activating only a small number of experts for each token. This makes the router very important, because it decides which experts see data and receive gradients. If routing is imbalanced, some experts can be heavily trained while others are almost unused. Recent work also suggests that routing patterns often reflect hidden-state geometry, rather than directly proving human-interpretable domain expertise. So I treat routing as a geometric mechanism first.",
  },
  {
    no: "03",
    title: "Question: which geometry does top-1 routing amplify first?",
    bullets: [
      "Working thesis: hidden states contain useful residual structure, but also a shared common direction.",
      "A linear top-1 router can turn that common direction into expert-specific offsets.",
      "Current question: can expert-aware initialization reduce early bias, or does training re-amplify it?",
    ],
    image: "s03_storyline_ladder.png",
    caption: "Seven-day story: false specialization signal -> common-logit audit -> expert-spectrum stress test.",
    notes:
      "The working thesis is that hidden states contain useful residual structure, but they also contain a shared common direction. A linear top-1 router can turn this common direction into different scores for different experts. My current question is whether an expert-aware initialization can reduce this early bias, or whether training quickly re-amplifies the bias.",
  },
  {
    no: "04",
    title: "High route consistency can hide collapse",
    bullets: [
      "A feature can route consistently while many features still share one expert.",
      "Consistency alone is not evidence of useful specialization.",
      "The audit must track load, assignment structure, and intervention response together.",
    ],
    image: "s04_baseline_collapse_heatmaps_cropped.png",
    caption: "Same-looking consistency can coexist with collapsed expert usage.",
    notes:
      "This matters because route consistency can be misleading. A feature may be routed consistently, but many different features can still collapse into the same expert. In that case, consistency looks good, but expert usage is not specialized. Therefore I track load, assignment structure, and intervention response together, instead of relying on one metric.",
  },
  {
    no: "05",
    title: "Specialization is reachable, but random top-1 often misses the basin",
    bullets: [
      "Slot-aware initialization produces stable slot-to-expert structure.",
      "Oracle-to-trainable release can preserve specialization after basin entry.",
      "The bottleneck is early basin entry, not impossibility of specialization.",
    ],
    image: "s05_slot_init_positive_control_heatmaps_cropped.png",
    caption: "Positive control: the model can specialize when the early basin is controlled.",
    notes:
      "The positive-control experiments show that specialization is reachable. When the router is initialized with slot information, the model can form stable slot-to-expert structure. When an oracle router is released into a trainable router after a good basin is reached, specialization can also remain stable. This means the bottleneck is not that specialization is impossible. The bottleneck is how the model enters the right basin in early training.",
  },
  {
    no: "06",
    title: "Common-logit bias acts like an expert-specific offset",
    bullets: [
      "Decompose router input: h_i = c + r_i.",
      "Gate score: z_{i,e} = w_e^T c + w_e^T r_i.",
      "The common term is token-shared but expert-dependent, so it can win top-1 before residual features matter.",
    ],
    image: "s06_common_logit_model.png",
    caption: "Mechanism candidate: shared input geometry becomes unequal expert scores.",
    notes:
      "The mechanism candidate is common-logit bias. I decompose the router input as a common component plus a residual component. Then the gate score has two parts: the expert's projection on the common component, and the expert's projection on the residual token-specific component. The common part is shared across tokens, but it differs across experts, so it acts like an expert-specific offset. In top-1 routing, this offset can win before useful residual features become decisive.",
  },
  {
    no: "07",
    title: "Controlled evidence: common-logit appears early and is intervention-relevant",
    bullets: [
      "Common margin rises before slot margin becomes decisive.",
      "Common-logit cancellation improves slot NMI while preserving accuracy.",
      "This supports common-logit as a causal contributor in the controlled setting.",
    ],
    images: ["s07_common_vs_slot_margin_timing.png", "s07_common_cancellation_metrics.png"],
    caption: "Intervention result: slot NMI improves while accuracy stays at 1.000.",
    notes:
      "In controlled settings, this common-logit signal appears early. The common margin rises before the slot margin becomes decisive. More importantly, when I cancel the common-logit term, slot NMI improves strongly while accuracy stays unchanged. This supports common-logit as a causal contributor in the controlled setting, not just a post-hoc explanation.",
  },
  {
    no: "08",
    title: "Real-text step 0: common direction matters, but it is not the whole story",
    bullets: [
      "After removing top-1% high-frequency tokens, random linear routers still show step-0 load bias.",
      "Centering / common removal reduces the bias, but does not eliminate all structure.",
      "This moves the question from static bias to early training amplification.",
    ],
    images: ["s09_realtext_step0_common_vs_residual.png", "s09_realtext_raw_vs_centered_load.png"],
    caption: "Real text narrows the claim: static common removal is useful, but incomplete.",
    notes:
      "Real text makes the claim narrower. After removing the top one percent high-frequency tokens, random linear routers still show load bias at step 0. Centering or common removal reduces the bias, but it does not remove all structure. So the real-text question is no longer only whether a static common direction exists. The sharper question is how early training amplifies or reshapes that bias.",
  },
  {
    no: "09",
    title: "Step-10 concentration is a coupled gate-hidden effect",
    bullets: [
      "Freezing only the router or only the experts does not explain the full spike.",
      "Freezing the prefix before layer 5 suppresses most early amplification.",
      "Replay shows a large interaction between router updates and hidden-state changes.",
    ],
    images: ["s11_freeze_split_key_numbers.png", "s11_replay_heatmap_common_margin.png"],
    caption: "0614 update: early concentration is not gate-only.",
    notes:
      "The June 14 result addresses that dynamic question. Freezing only the router or only the experts does not explain the full step-10 spike. Freezing the prefix before layer 5 suppresses most of the amplification. Cross-checkpoint replay also shows a large interaction between router updates and hidden-state changes. This means step-10 concentration is a coupled gate-hidden effect, not a gate-only effect.",
  },
  {
    no: "10",
    title: "0615 test: initialize the router from expert input geometry",
    bullets: [
      "Expert principal input subspaces are measurable and differ across experts.",
      "Their overlap with the hidden-state common direction is low.",
      "The idea is computationally meaningful, but not yet a specialization claim.",
    ],
    metrics: [
      ["expert-expert subspace overlap", "0.0116"],
      ["expert-common overlap", "0.0166"],
      ["raw spectrum utility correlation", "0.2328"],
    ],
    kind: "pipeline",
    notes:
      "This motivates the June 15 initialization test. The idea is to initialize the router from each expert's principal input geometry. For each expert, I estimate its principal input subspace from the initial expert matrices. These subspaces are measurable and differ across experts, with low expert-expert overlap. They also have low overlap with the hidden-state common direction. Therefore the idea is computationally meaningful, but it does not yet imply semantic expert specialization.",
  },
  {
    no: "11",
    title: "Common-filtered spectrum improves step 0, but fails by step 10",
    bullets: [
      "Step 0 after removing top-1% high-frequency tokens: max load improves from 19.98% to 13.97%.",
      "Step 10: max load worsens from 83.16% to 93.51%.",
      "Better initialization balance does not guarantee stable early routing dynamics.",
    ],
    image: "s12_0615_spectrum_init_stress_test.png",
    caption: "0615 verdict: supported at step 0; not supported at step 10.",
    notes:
      "The result is mixed and informative. After removing the top one percent high-frequency tokens, common-filtered expert-spectrum initialization improves step-0 balance: the maximum expert load drops from 19.98 percent to 13.97 percent. But after 10 training steps, the maximum load becomes worse: 93.51 percent, compared with 83.16 percent for random initialization. So the initialization fixes part of the starting bias, but it does not control early training amplification.",
  },
  {
    no: "12",
    title: "Three conclusions: geometry is useful, but initialization is not enough",
    conclusions: [
      ["Expert geometry exists", "Input subspaces differ and are not the common direction."],
      ["Step-0 bias can improve", "Common-filtered spectrum reduces initial max load."],
      ["Step-10 needs dynamics", "Router-hidden-state amplification dominates initialization alone."],
    ],
    next:
      "Next decision: audit whether step-0 route winners are reinforced by early hidden-state change and router updates. Branch: test an oracle or learned bridge for expert-spectrum matching.",
    image: "s12_next_mechanism_hypothesis.png",
    notes:
      "The updated conclusion has three parts. First, expert input geometry is measurable and not identical to the common direction. Second, common-filtered initialization can reduce step-0 load bias. Third, step-10 concentration is driven by early router-hidden-state amplification, not initialization alone. Therefore I should not simply scale the current linear initialization experiment. The next main decision is to audit whether step-0 route winners are reinforced by hidden-state change and router updates. A branch question is whether an oracle or learned bridge can express expert-spectrum matching better than the current linear top-1 router.",
  },
  {
    no: "13",
    title: "Backup: what this result does and does not claim",
    kind: "boundary",
    canSay: [
      "Expert-spectrum directions are measurable and differ across experts.",
      "Common-filtered initialization improves step-0 balance.",
      "Current linear top-1 initialization cannot prevent step-10 concentration.",
    ],
    cannotSay: [
      "Expert spectrum is useless.",
      "Domain specialization has been explained.",
      "The result generalizes to pretrained large MoEs, top-2/top-4 routing, or load-balancing losses.",
    ],
    notes:
      "The claim boundary is important. I can say that expert-spectrum directions are measurable, that common-filtered initialization improves step-0 balance, and that the current linear top-1 initialization cannot prevent step-10 concentration. I cannot say that expert spectrum is useless, or that domain specialization has been fully explained, or that this result generalizes to pretrained large MoEs and other routing settings.",
  },
  {
    no: "14",
    title: "Backup: references",
    kind: "refs",
    refs: [
      "Shazeer et al., Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer, 2017.",
      "Fedus et al., Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity, 2021.",
      "Zoph et al., ST-MoE: Designing Stable and Transferable Sparse Expert Models, 2022.",
      "Wang et al., The Myth of Expert Specialization in MoEs, 2026.",
      "Ahrac et al., Routers Learn the Geometry of Their Experts, 2026.",
    ],
    notes:
      "These are the references I use to position the project. The classical MoE papers define the routing and load-balancing problem. The recent geometry papers motivate my claim boundary: routing geometry is meaningful, but it should not be confused with semantic domain expertise.",
  },
];

function addShape(slide, opts, text, style = {}) {
  const shape = slide.shapes.add({
    geometry: opts.geometry || "textbox",
    name: opts.name,
    position: opts.position,
    fill: opts.fill ?? "none",
    line: opts.line ?? { style: "solid", fill: "none", width: 0 },
    borderRadius: opts.borderRadius,
    shadow: opts.shadow,
  });
  if (text !== undefined) {
    shape.text = text;
    shape.text.style = {
      typeface: font,
      fontSize: 18,
      color: c.ink,
      lineSpacing: 1.1,
      insets: { top: 4, right: 4, bottom: 4, left: 4 },
      ...style,
    };
  }
  return shape;
}

function addHeader(slide, s) {
  slide.background.fill = c.white;
  slide.shapes.add({
    geometry: "rect",
    position: { left: 0, top: 0, width: W, height: 8 },
    fill: c.magenta,
    line: { style: "solid", fill: "none", width: 0 },
  });
  addShape(
    slide,
    { position: { left: page.left, top: 30, width: 880, height: 56 } },
    s.title,
    { fontSize: 31, bold: true, color: c.ink, lineSpacing: 0.98, autoFit: "shrinkText" },
  );
  addShape(
    slide,
    { position: { left: 1084, top: 36, width: 120, height: 24 } },
    `${s.no}/14`,
    { fontSize: 12, color: c.muted, alignment: "right" },
  );
  slide.shapes.add({
    geometry: "line",
    position: { left: page.left, top: 94, width: page.width, height: 0 },
    fill: "none",
    line: { style: "solid", fill: c.line, width: 1 },
  });
}

function bulletText(items) {
  return items.map((x) => `- ${x}`).join("\n");
}

function addBullets(slide, items, pos, fontSize = 20) {
  return addShape(slide, { position: pos }, bulletText(items), {
    fontSize,
    color: c.ink,
    lineSpacing: 1.18,
    autoFit: "shrinkText",
  });
}

async function addImage(slide, readImageBlob, imageName, pos, alt, fit = "contain") {
  const blob = await readImageBlob(path.join(FIG, imageName));
  slide.images.add({
    blob,
    contentType: "image/png",
    alt: alt || imageName,
    fit,
    position: pos,
  });
}

function addCaption(slide, text, pos) {
  addShape(
    slide,
    {
      geometry: "roundRect",
      position: pos,
      fill: c.light,
      line: { style: "solid", fill: c.line, width: 1 },
      borderRadius: 8,
    },
    text,
    { fontSize: 15, color: c.magentaDark, bold: true, alignment: "center", verticalAlignment: "middle" },
  );
}

async function renderStandardSlide(slide, s, readImageBlob) {
  addHeader(slide, s);
  if (s.no === "04" || s.no === "05") {
    addBullets(slide, s.bullets, { left: page.left, top: 122, width: 1000, height: 125 }, 20);
    await addImage(slide, readImageBlob, s.image, { left: 94, top: 295, width: 1092, height: 150 }, s.title);
    if (s.caption) addCaption(slide, s.caption, { left: page.left, top: 620, width: page.width, height: 38 });
    return;
  }
  addBullets(slide, s.bullets, { left: page.left, top: 122, width: 430, height: 230 }, 20);
  if (s.image) {
    await addImage(slide, readImageBlob, s.image, { left: 545, top: 122, width: 640, height: 420 }, s.title);
  }
  if (s.inset) {
    addShape(slide, {
      geometry: "roundRect",
      position: { left: 944, top: 425, width: 230, height: 126 },
      fill: c.white,
      line: { style: "solid", fill: c.line, width: 1 },
      borderRadius: 8,
      shadow: "shadow-sm",
    });
    await addImage(slide, readImageBlob, s.inset, { left: 956, top: 436, width: 206, height: 104 }, "inset");
  }
  if (s.images) {
    await addImage(slide, readImageBlob, s.images[0], { left: 516, top: 126, width: 328, height: 360 }, s.images[0]);
    await addImage(slide, readImageBlob, s.images[1], { left: 864, top: 126, width: 328, height: 360 }, s.images[1]);
  }
  if (s.caption) addCaption(slide, s.caption, { left: page.left, top: 620, width: page.width, height: 38 });
}

async function renderTitle(slide, s, readImageBlob) {
  slide.background.fill = c.white;
  slide.shapes.add({
    geometry: "rect",
    position: { left: 0, top: 0, width: 18, height: H },
    fill: c.magenta,
    line: { style: "solid", fill: "none", width: 0 },
  });
  slide.shapes.add({
    geometry: "rect",
    position: { left: 18, top: 0, width: 8, height: H },
    fill: c.blue,
    line: { style: "solid", fill: "none", width: 0 },
  });
  addShape(slide, { position: { left: 86, top: 88, width: 650, height: 42 } }, s.kicker, {
    fontSize: 16,
    bold: true,
    color: c.magenta,
  });
  addShape(slide, { position: { left: 82, top: 152, width: 650, height: 220 } }, s.title, {
    fontSize: 47,
    bold: true,
    color: c.ink,
    lineSpacing: 0.92,
    autoFit: "shrinkText",
  });
  addShape(slide, { position: { left: 86, top: 402, width: 650, height: 78 } }, s.subtitle, {
    fontSize: 23,
    color: c.muted,
    lineSpacing: 1.08,
  });
  addCaption(slide, "Mechanism audit | not a finished-method claim", {
    left: 86,
    top: 555,
    width: 520,
    height: 42,
  });
  await addImage(slide, readImageBlob, s.image, { left: 760, top: 118, width: 430, height: 410 }, s.title);
}

function addPipeline(slide) {
  const y = 305;
  const boxes = [
    ["Expert input matrices", "gate_proj + up_proj"],
    ["Principal subspaces", "top eigen-directions"],
    ["Common filtering", "remove shared token direction"],
    ["Linear top-1 router", "current implementation bridge"],
  ];
  const x0 = 520;
  const gap = 24;
  const bw = 150;
  for (let i = 0; i < boxes.length; i += 1) {
    const x = x0 + i * (bw + gap);
    addShape(
      slide,
      {
        geometry: "roundRect",
        position: { left: x, top: y, width: bw, height: 112 },
        fill: i === boxes.length - 1 ? "#FFF6FB" : c.light,
        line: { style: "solid", fill: i === boxes.length - 1 ? c.magenta : c.line, width: 1.4 },
        borderRadius: 8,
      },
      `${boxes[i][0]}\n${boxes[i][1]}`,
      { fontSize: 17, bold: i === 0, color: c.ink, alignment: "center", verticalAlignment: "middle" },
    );
    if (i < boxes.length - 1) {
      slide.shapes.add({
        geometry: "rightArrow",
        position: { left: x + bw + 3, top: y + 39, width: gap + 18, height: 34 },
        fill: c.blue,
        line: { style: "solid", fill: "none", width: 0 },
      });
    }
  }
}

function renderPipelineSlide(slide, s) {
  addHeader(slide, s);
  addBullets(slide, s.bullets, { left: page.left, top: 122, width: 430, height: 230 }, 20);
  const mx = page.left;
  for (let i = 0; i < s.metrics.length; i += 1) {
    const [label, value] = s.metrics[i];
    addShape(
      slide,
      {
        geometry: "roundRect",
        position: { left: mx, top: 392 + i * 64, width: 430, height: 48 },
        fill: c.light,
        line: { style: "solid", fill: c.line, width: 1 },
        borderRadius: 8,
      },
      `${value}    ${label}`,
      { fontSize: 18, bold: true, color: i === 2 ? c.magenta : c.ink, verticalAlignment: "middle" },
    );
  }
  addPipeline(slide);
  addCaption(slide, "Interpretation: computable basis, strict claim boundary.", {
    left: 520,
    top: 476,
    width: 674,
    height: 40,
  });
}

async function renderConclusion(slide, s, readImageBlob) {
  addHeader(slide, s);
  for (let i = 0; i < s.conclusions.length; i += 1) {
    const [head, body] = s.conclusions[i];
    const x = page.left + i * 382;
    addShape(
      slide,
      {
        geometry: "roundRect",
        position: { left: x, top: 125, width: 344, height: 130 },
        fill: i === 2 ? "#FFF5FB" : c.light,
        line: { style: "solid", fill: i === 2 ? c.magenta : c.line, width: 1.2 },
        borderRadius: 8,
      },
      `${i + 1}. ${head}\n${body}`,
      { fontSize: 19, bold: true, color: c.ink, lineSpacing: 1.08, autoFit: "shrinkText" },
    );
  }
  await addImage(slide, readImageBlob, s.image, { left: 140, top: 285, width: 420, height: 250 }, s.image);
  addShape(
    slide,
    {
      geometry: "roundRect",
      position: { left: 610, top: 302, width: 520, height: 210 },
      fill: c.white,
      line: { style: "solid", fill: c.line, width: 1.2 },
      borderRadius: 8,
      shadow: "shadow-sm",
    },
    s.next,
    { fontSize: 21, bold: true, color: c.magentaDark, lineSpacing: 1.12, autoFit: "shrinkText" },
  );
  addCaption(slide, "Research decision: mechanism audit first; stronger routing bridge second.", {
    left: page.left,
    top: 620,
    width: page.width,
    height: 38,
  });
}

function renderBoundary(slide, s) {
  addHeader(slide, s);
  addShape(
    slide,
    {
      geometry: "roundRect",
      position: { left: page.left, top: 138, width: 520, height: 410 },
      fill: "#F4FBF8",
      line: { style: "solid", fill: "#B9DED2", width: 1.2 },
      borderRadius: 8,
    },
    `Can say\n${bulletText(s.canSay)}`,
    { fontSize: 20, bold: true, color: c.green, lineSpacing: 1.18, autoFit: "shrinkText" },
  );
  addShape(
    slide,
    {
      geometry: "roundRect",
      position: { left: 684, top: 138, width: 520, height: 410 },
      fill: "#FFF7F5",
      line: { style: "solid", fill: "#F1B5AD", width: 1.2 },
      borderRadius: 8,
    },
    `Cannot say\n${bulletText(s.cannotSay)}`,
    { fontSize: 20, bold: true, color: c.red, lineSpacing: 1.18, autoFit: "shrinkText" },
  );
}

function renderRefs(slide, s) {
  addHeader(slide, s);
  addShape(
    slide,
    { position: { left: 108, top: 130, width: 1040, height: 420 } },
    s.refs.map((r) => `- ${r}`).join("\n\n"),
    { fontSize: 20, color: c.ink, lineSpacing: 1.12, autoFit: "shrinkText" },
  );
  addCaption(slide, "Positioning: classic MoE scaling problem + recent geometry-based claim boundary.", {
    left: page.left,
    top: 620,
    width: page.width,
    height: 38,
  });
}

async function main() {
  process.env.HOME ||= "C:\\Users\\250010109";
  const { Presentation, PresentationFile, readImageBlob, saveBlobToFile } = await loadArtifactTool();
  await fs.mkdir(OUT, { recursive: true });

  const presentation = Presentation.create({ slideSize: { width: W, height: H } });
  presentation.theme.colorScheme = {
    name: "HETAU-inspired Academic",
    themeColors: {
      accent1: c.magenta,
      accent2: c.blue,
      accent3: c.yellow,
      accent4: c.pink,
      accent5: c.green,
      accent6: c.red,
      bg1: c.white,
      bg2: c.light,
      tx1: c.ink,
      tx2: c.muted,
      dk1: "#000000",
      dk2: c.magentaDark,
      lt1: c.white,
      lt2: c.line,
      hlink: c.blue,
      folHlink: c.magenta,
    },
  };

  for (const spec of slides) {
    const slide = presentation.slides.add();
    if (spec.kind === "title") await renderTitle(slide, spec, readImageBlob);
    else if (spec.kind === "pipeline") renderPipelineSlide(slide, spec);
    else if (spec.kind === "boundary") renderBoundary(slide, spec);
    else if (spec.kind === "refs") renderRefs(slide, spec);
    else if (spec.conclusions) await renderConclusion(slide, spec, readImageBlob);
    else await renderStandardSlide(slide, spec, readImageBlob);
    slide.speakerNotes.textFrame.setText(spec.notes || "");
    slide.speakerNotes.setVisible(true);
  }

  for (const [index, slide] of presentation.slides.items.entries()) {
    const stem = `slide-${String(index + 1).padStart(2, "0")}`;
    await saveBlobToFile(await presentation.export({ slide, format: "png", scale: 1 }), path.join(OUT, `${stem}.png`));
    await fs.writeFile(path.join(OUT, `${stem}.layout.json`), await (await slide.export({ format: "layout" })).text());
  }
  await saveBlobToFile(
    await presentation.export({
      format: "webp",
      montage: { columns: 2, padding: 20, gap: 14, background: "#FFFFFF" },
      scale: 1,
    }),
    path.join(OUT, "deck_montage.webp"),
  );

  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(path.join(OUT, "project2_12min_deck_0615.pptx"));
  console.log(path.join(OUT, "project2_12min_deck_0615.pptx"));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
