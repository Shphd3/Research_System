$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$Root = "C:\Users\250010109\data\Research_System"
$Template = Join-Path $Root "Projects\academic_writing\resources\ppt_templates\hetau_college_ppt_template_0709.pptx"
$Pack = Join-Path $Root "Projects\academic_writing\main\slides\0615_ppt_content_pack"
$Fig = Join-Path $Pack "figures"
$Out = Join-Path $Pack "pptx_output_template_based"
$Final = Join-Path $Out "project2_12min_deck_0615_template_based.pptx"
$Preview = Join-Path $Out "preview"
New-Item -ItemType Directory -Force -Path $Out, $Preview | Out-Null

$ppLayoutBlank = 12
$msoTextOrientationHorizontal = 1
$msoTrue = -1
$msoFalse = 0
$msoShapeRectangle = 1
$msoShapeRoundedRectangle = 5
$msoShapeRightArrow = 33
$msoShapeOval = 9
$ppSaveAsOpenXMLPresentation = 24

function C($hex) {
  $h = $hex.TrimStart("#")
  $r = [Convert]::ToInt32($h.Substring(0,2),16)
  $g = [Convert]::ToInt32($h.Substring(2,2),16)
  $b = [Convert]::ToInt32($h.Substring(4,2),16)
  return $r + ($g * 256) + ($b * 65536)
}

$Color = @{
  Magenta = C "#881E55"
  Magenta2 = C "#D14AA4"
  Pink = C "#E27DBE"
  PalePink = C "#F7EAF2"
  PaleGray = C "#F4F2F5"
  Blue = C "#29AAE3"
  Yellow = C "#FBB900"
  Ink = C "#17141A"
  Muted = C "#5B5960"
  White = C "#FFFFFF"
  Line = C "#DED8E2"
  Green = C "#0E7A63"
  Red = C "#B42318"
}

$StudentName = "$([char]0x9093)$([char]0x661F)$([char]0x5B87) Deng Xingyu | Student ID: 250010109"

function Clear-Slide($slide) {
  for ($i = $slide.Shapes.Count; $i -ge 1; $i--) {
    try { $slide.Shapes.Item($i).Delete() } catch {}
  }
}

function Add-Text($slide, $text, $x, $y, $w, $h, $size=18, $color=$Color.Ink, $bold=$false, $align=1) {
  try {
    $shape = $slide.Shapes.AddTextbox($msoTextOrientationHorizontal, $x, $y, $w, $h)
  } catch {
    $preview = [string]$text
    if ($preview.Length -gt 80) { $preview = $preview.Substring(0,80) }
    throw "Add-Text failed: x=$x y=$y w=$w h=$h text=$preview :: $($_.Exception.Message)"
  }
  $shape.TextFrame.MarginLeft = 0
  $shape.TextFrame.MarginRight = 0
  $shape.TextFrame.MarginTop = 0
  $shape.TextFrame.MarginBottom = 0
  $shape.TextFrame.WordWrap = $msoTrue
  $shape.TextFrame.TextRange.Text = $text
  $shape.TextFrame.TextRange.Font.Name = $(if ($bold -or $size -ge 22) { "HarmonyOS Sans Black" } else { "HarmonyOS Sans" })
  $shape.TextFrame.TextRange.Font.Size = $size
  $shape.TextFrame.TextRange.Font.Color.RGB = $color
  $shape.TextFrame.TextRange.Font.Bold = $(if ($bold) { $msoTrue } else { $msoFalse })
  $shape.TextFrame.TextRange.ParagraphFormat.Alignment = $align
  return $shape
}

function Add-Box($slide, $x, $y, $w, $h, $fill, $line=$null, $radius=$true) {
  $type = $(if ($radius) { $msoShapeRoundedRectangle } else { $msoShapeRectangle })
  $shape = $slide.Shapes.AddShape($type, $x, $y, $w, $h)
  $shape.Fill.Visible = $msoTrue
  $shape.Fill.ForeColor.RGB = $fill
  if ($line -eq $null) {
    $shape.Line.Visible = $msoFalse
  } else {
    $shape.Line.Visible = $msoTrue
    $shape.Line.ForeColor.RGB = $line
    $shape.Line.Weight = 1
  }
  return $shape
}

function Add-Header($slide, $title, $num) {
  Add-Text $slide $title 42 72 790 32 24 $Color.Ink $true | Out-Null
  Add-Text $slide ("{0}/{1}" -f $num.ToString("00"), $Script:TotalSlides) 870 55 50 16 8 $Color.Muted $false 3 | Out-Null
  $line = $slide.Shapes.AddShape($msoShapeRectangle, 42, 106, 876, 1.2)
  $line.Fill.ForeColor.RGB = $Color.Line
  $line.Line.Visible = $msoFalse
}

function Add-Bullets($slide, $items, $x, $y, $w, $h, $size=15) {
  $text = ($items | ForEach-Object { "- " + $_ }) -join "`r"
  return Add-Text $slide $text $x $y $w $h $size $Color.Ink $false
}

function Add-Citation($slide, $text) {
  Add-Text $slide $text 52 492 840 14 8 $Color.Muted $false | Out-Null
}

function Set-Notes($slide, $text) {
  try {
    $placeholder = $slide.NotesPage.Shapes.Placeholders(2)
    $placeholder.TextFrame.TextRange.Text = $text
  } catch {
    try {
      for ($n=1; $n -le $slide.NotesPage.Shapes.Count; $n++) {
        $shape = $slide.NotesPage.Shapes.Item($n)
        if ($shape.HasTextFrame) {
          $shape.TextFrame.TextRange.Text = $text
          break
        }
      }
    } catch {}
  }
}

function Add-ConclusionBar($slide, $idx, $head, $body, $x, $y, $w, $h, $fill, $textColor) {
  Add-Box $slide $x $y $w $h $fill $null $false | Out-Null
  Add-Text $slide $idx ($x+18) ($y+8) 92 ($h-12) 44 $textColor $true 2 | Out-Null
  Add-Text $slide $head ($x+118) ($y+18) ($w-150) 22 15 $textColor $true | Out-Null
  Add-Text $slide $body ($x+118) ($y+44) ($w-150) 34 11 $textColor $false | Out-Null
}

function Add-ImageContain($slide, $file, $x, $y, $w, $h) {
  $img = [System.Drawing.Image]::FromFile($file)
  try {
    $ratio = $img.Width / $img.Height
    $box = $w / $h
    if ($ratio -gt $box) {
      $nw = $w
      $nh = $w / $ratio
      $nx = $x
      $ny = $y + ($h - $nh) / 2
    } else {
      $nh = $h
      $nw = $h * $ratio
      $nx = $x + ($w - $nw) / 2
      $ny = $y
    }
  } finally {
    $img.Dispose()
  }
  $pic = $slide.Shapes.AddPicture($file, $msoFalse, $msoTrue, $nx, $ny, $nw, $nh)
  return $pic
}

function Add-ImageFill($slide, $file, $x, $y, $w, $h) {
  return $slide.Shapes.AddPicture($file, $msoFalse, $msoTrue, $x, $y, $w, $h)
}

function Add-FigurePanel($slide, $file, $x, $y, $w, $h, $label="") {
  Add-Box $slide $x $y $w $h $Color.White $Color.Line | Out-Null
  Add-ImageContain $slide (Join-Path $Fig $file) ($x+8) ($y+8) ($w-16) ($h-22) | Out-Null
  if ($label) { Add-Text $slide $label ($x+12) ($y+$h-17) ($w-24) 12 8 $Color.Muted $false 2 | Out-Null }
}

function Add-StatCard($slide, $value, $label, $x, $y, $w, $h, $fill=$Color.PalePink, $accent=$Color.Magenta) {
  Add-Box $slide $x $y $w $h $fill $Color.Line | Out-Null
  if ($h -lt 58) {
    Add-Text $slide "$value — $label" ($x+12) ($y+13) ($w-24) ($h-18) 12 $accent $true | Out-Null
  } else {
    Add-Text $slide $value ($x+12) ($y+12) ($w-24) 30 24 $accent $true | Out-Null
    Add-Text $slide $label ($x+12) ($y+48) ($w-24) ([Math]::Max(12, $h-54)) 10 $Color.Ink $true | Out-Null
  }
}

function Add-Pipeline($slide, $labels, $x, $y, $w, $h) {
  $gap = 12
  $bw = ($w - $gap * ($labels.Count - 1)) / $labels.Count
  for ($i=0; $i -lt $labels.Count; $i++) {
    $bx = $x + $i * ($bw + $gap)
    $fill = @($Color.Magenta2, $Color.Pink, $Color.PaleGray, $Color.Magenta)[$i % 4]
    Add-Box $slide $bx $y $bw $h $fill $Color.Line | Out-Null
    $tc = $(if ($i -eq 0 -or $i -eq 1 -or $i -eq 3) { $Color.White } else { $Color.Ink })
    Add-Text $slide $labels[$i] ($bx+10) ($y+16) ($bw-20) ($h-24) 12 $tc $true 2 | Out-Null
    if ($i -lt $labels.Count - 1) {
      $arr = $slide.Shapes.AddShape($msoShapeRightArrow, ($bx+$bw-2), ($y+$h/2-8), 18, 16)
      $arr.Fill.ForeColor.RGB = $Color.Blue
      $arr.Line.Visible = $msoFalse
    }
  }
}

function Add-ConclusionCard($slide, $idx, $head, $body, $x, $y, $w, $h, $strong=$false) {
  $fill = $(if ($strong) { C "#F9EAF2" } else { $Color.PaleGray })
  $line = $(if ($strong) { $Color.Magenta } else { $Color.Line })
  Add-Box $slide $x $y $w $h $fill $line | Out-Null
  Add-Text $slide "$idx" ($x+12) ($y+10) 34 40 28 $(if ($strong){$Color.Magenta}else{$Color.Pink}) $true | Out-Null
  Add-Text $slide $head ($x+54) ($y+14) ($w-66) 22 14 $Color.Ink $true | Out-Null
  Add-Text $slide $body ($x+54) ($y+44) ($w-66) ($h-54) 11 $Color.Ink $false | Out-Null
}

$Slides = @(
  @{base=2; kind="cover"},
  @{base=10; title="Agenda"; kind="agenda"},
  @{base=15; title="MoE scaling is router-limited, not only expert-limited"; kind="background"},
  @{base=10; title="Question: which geometry does top-1 routing amplify first?"; kind="question"},
  @{base=15; title="High route consistency can hide collapse"; kind="heatmap_false"},
  @{base=15; title="Specialization is reachable, but random top-1 often misses the basin"; kind="heatmap_positive"},
  @{base=4; title="Common-logit bias acts like an expert-specific offset"; kind="mechanism"},
  @{base=3; title="Controlled evidence: common-logit appears early"; kind="controlled"},
  @{base=3; title="Real-text step 0: common direction matters, but is incomplete"; kind="realtext"},
  @{base=3; title="Step-10 concentration is a coupled gate-hidden effect"; kind="coupled"},
  @{base=10; title="Expert-spectrum test: initialize the router from expert input geometry"; kind="method"},
  @{base=15; title="Common-filtered spectrum improves step 0, but fails by step 10"; kind="result"},
  @{base=15; title="Three conclusions: geometry is useful, but initialization is not enough"; kind="conclusion"},
  @{base=15; title="Backup: what this result does and does not claim"; kind="boundary"},
  @{base=15; title="Backup: references"; kind="refs"}
)
$Script:TotalSlides = $Slides.Count

$Script:Notes = @{
  cover = @'
Timing: 35s.
I will present a mechanism audit of sparse MoE routing. The goal is not to claim a finished routing method. The question is why a top-1 router can concentrate many tokens onto a few experts before useful specialization forms. The final part tests an expert-spectrum initialization idea and shows that initialization alone is not enough.
'@
  agenda = @'
Timing: 35s.
The talk has six parts. I first motivate why routing geometry matters for sparse MoE scaling. Then I define the research question. The middle part gives the common-logit mechanism and training-dynamics evidence. The last part presents the expert-spectrum stress test, the claim boundary, and the next decision.
'@
  background = @'
Timing: 50s.
Sparse MoE increases parameter count while activating only a few experts per token. That makes the router the bottleneck: it controls which experts see data and receive gradients. Prior MoE work studies scaling and load balance. Recent geometry work adds a warning: routing patterns can reflect hidden-state geometry rather than semantic expertise. I use that boundary throughout this talk.
'@
  question = @'
Timing: 45s.
The working thesis is simple. Hidden states may contain useful residual structure, but they also contain a shared common direction. A linear top-1 router can convert that shared direction into expert-specific offsets. The research question is whether expert-aware initialization can reduce the early bias, or whether training quickly amplifies it again.
'@
  heatmap_false = @'
Timing: 45s.
This slide explains why route consistency alone is not enough. A feature may route consistently, but many different features can still share one expert. That is a false positive for specialization. So I track three things together: expert load, assignment structure, and whether an intervention changes the routing pattern.
'@
  heatmap_positive = @'
Timing: 50s.
This positive control rules out a weak explanation. The model is not fundamentally unable to specialize. When the early routing basin is controlled by slot-aware initialization or oracle release, stable slot-to-expert structure can appear. Therefore the bottleneck is basin entry during early training, not the impossibility of specialization.
'@
  mechanism = @'
Timing: 60s.
The mechanism is common-logit bias. I decompose the hidden state as h_i equals c plus r_i. The gate score then contains a common term and a residual term. The common term is shared across tokens, but its value differs across experts because each expert has a different router weight. Under top-1 routing, this term can act like an expert-specific offset.
'@
  controlled = @'
Timing: 50s.
In the controlled setting, common-logit appears before the slot margin becomes decisive. More importantly, cancelling the common-logit improves slot NMI while preserving accuracy. This makes the mechanism intervention-relevant, not just descriptive. It supports the idea that a shared direction can distort early top-1 routing.
'@
  realtext = @'
Timing: 50s.
Real text narrows the claim. After removing the top one percent high-frequency tokens, random linear routers still show step-zero load bias. Centering or common removal reduces that bias, but it does not remove all structure. So the real problem is not only static initialization bias; it is how early training amplifies or reshapes that bias.
'@
  coupled = @'
Timing: 55s.
The training-dynamics audit shows that step-ten concentration is not gate-only. Freezing only the router or only experts does not explain the full spike. Freezing the prefix before layer 5 suppresses most amplification, and replay shows a large router-hidden-state interaction. This predicts that a purely linear initialization may help at step zero but fail after updates.
'@
  method = @'
Timing: 55s.
The expert-spectrum test initializes the router from each expert's principal input geometry. These expert subspaces are measurable, differ across experts, and have low overlap with the hidden-state common direction. That makes the idea computationally meaningful. But it is still not a claim of semantic specialization; it is a routing-geometry initialization test.
'@
  result = @'
Timing: 60s.
The result is mixed and informative. After filtering the common direction, step-zero balance improves: max expert load drops from 19.98 percent to 13.97 percent. But after ten steps, max load becomes worse: 93.51 percent compared with 83.16 percent for random initialization. The conclusion is precise: better initial balance does not control early training amplification.
'@
  conclusion = @'
Timing: 60s.
The updated conclusion has three parts. First, expert geometry exists and is not identical to the common direction. Second, common-filtered initialization improves step-zero balance. Third, step-ten concentration is driven by router-hidden-state amplification, not initialization alone. The next decision is to audit whether early route winners are reinforced by hidden-state change and router updates.
'@
  boundary = @'
Backup only.
This is the claim boundary. I can claim measurable expert-spectrum directions, improved step-zero balance, and failure of the current linear top-1 initialization to prevent step-ten concentration. I cannot claim expert spectrum is useless, that domain specialization is explained, or that the result generalizes to larger pretrained MoEs or different routing settings.
'@
  refs = @'
Backup only.
These references position the project. The classical MoE papers define sparse routing and load-balancing concerns. The recent geometry papers motivate the claim boundary: routing geometry is meaningful, but it should not be confused with semantic domain expertise.
'@
}

$ppt = $null; $src = $null; $dst = $null
try {
  $ppt = New-Object -ComObject PowerPoint.Application
  $ppt.Visible = $msoTrue
  $ppt.DisplayAlerts = 1
  $src = $ppt.Presentations.Open($Template, $msoTrue, $msoFalse, $msoFalse)
  $dst = $ppt.Presentations.Add()
  $dst.PageSetup.SlideWidth = $src.PageSetup.SlideWidth
  $dst.PageSetup.SlideHeight = $src.PageSetup.SlideHeight
  while ($dst.Slides.Count -gt 0) { $dst.Slides.Item(1).Delete() }

  for ($si=0; $si -lt $Slides.Count; $si++) {
    $spec = $Slides[$si]
    $src.Slides.Item($spec.base).Copy()
    $range = $dst.Slides.Paste($dst.Slides.Count + 1)
    $slide = $range.Item(1)
    Clear-Slide $slide
    $num = $si + 1

    switch ($spec.kind) {
      "cover" {
        Add-Text $slide "Routers Learn the Geometry of Their Experts?" 60 94 780 42 24 $Color.White $true | Out-Null
        Add-Text $slide "Why Sparse MoE Routers Collapse Before They Specialize" 60 150 760 110 34 $Color.White $true | Out-Null
        Add-Text $slide "An audit of expert-spectrum initialization and early routing amplification" 62 282 660 44 17 $Color.White $false | Out-Null
        Add-Box $slide 62 380 370 54 (C "#FFFFFF") $null | Out-Null
        Add-Text $slide $StudentName 82 398 360 20 13 $Color.Magenta $true | Out-Null
        Add-Text $slide "Academic Writing Project 2 | 12-minute research update" 62 455 500 18 10 $Color.White $false | Out-Null
      }
      "agenda" {
        Add-Header $slide $spec.title $num
        Add-Text $slide "A mechanism audit, then a method stress test" 58 122 760 24 16 $Color.Magenta $true | Out-Null
        $agenda = @(
          @("01", "Motivation", "Why routing geometry matters for sparse MoE scaling."),
          @("02", "Research Question", "Which hidden-state geometry is amplified first?"),
          @("03", "Mechanism Evidence", "Common-logit bias in controlled and real-text settings."),
          @("04", "Training Dynamics", "Why step-10 concentration is not gate-only."),
          @("05", "Init Stress Test", "Expert-spectrum initialization improves step 0 but fails by step 10."),
          @("06", "Claim Boundary", "What can be claimed, what remains open.")
        )
        for ($ai=0; $ai -lt $agenda.Count; $ai++) {
          $row = [Math]::Floor($ai / 3)
          $col = $ai % 3
          $x = 58 + $col * 292
          $y = 172 + $row * 136
          $fill = @($Color.Magenta, $Color.Pink, $Color.PalePink, $Color.PaleGray, $Color.Magenta2, (C "#F4D5E6"))[$ai]
          Add-Box $slide $x $y 250 104 $fill $Color.Line | Out-Null
          $tc = $(if ($ai -eq 0 -or $ai -eq 1 -or $ai -eq 4) { $Color.White } else { $Color.Ink })
          Add-Text $slide $agenda[$ai][0] ($x+16) ($y+14) 44 34 26 $tc $true | Out-Null
          Add-Text $slide $agenda[$ai][1] ($x+66) ($y+18) 158 22 16 $tc $true | Out-Null
          Add-Text $slide $agenda[$ai][2] ($x+66) ($y+48) 158 40 10 $tc $false | Out-Null
        }
      }
      "background" {
        Add-Header $slide $spec.title $num
        Add-Box $slide 50 122 255 120 $Color.Magenta $null | Out-Null
        Add-Text $slide "Router controls who learns" 70 148 210 22 16 $Color.White $true | Out-Null
        Add-Text $slide "Sparse MoE activates few experts per token, so routing decides data and gradient flow." 70 178 210 42 12 $Color.White | Out-Null
        Add-Box $slide 332 122 255 120 $Color.Pink $null | Out-Null
        Add-Text $slide "Geometry before expertise" 352 148 210 22 16 $Color.White $true | Out-Null
        Add-Text $slide "Recent papers warn: routing patterns often reflect hidden-state geometry, not clean domains." 352 178 210 42 12 $Color.White | Out-Null
        Add-Box $slide 614 122 255 120 (C "#F4D5E6") $null | Out-Null
        Add-Text $slide "Our audit target" 634 148 210 22 16 $Color.Magenta $true | Out-Null
        Add-Text $slide "Which geometry does top-1 routing amplify before useful specialization forms?" 634 178 210 42 12 $Color.Ink | Out-Null
        Add-FigurePanel $slide "s02_background_gap_diagram.png" 88 270 780 176 "MoE promise -> router bottleneck -> early concentration failure"
        Add-Citation $slide "Refs: Shazeer et al., 2017; Fedus et al., 2021; Wang et al., 2026; Ahrac et al., 2026."
      }
      "question" {
        Add-Header $slide $spec.title $num
        Add-Box $slide 48 120 250 340 $Color.PalePink $Color.Line | Out-Null
        Add-Text $slide "Working thesis" 68 145 210 22 16 $Color.Magenta $true | Out-Null
        Add-Bullets $slide @(
          "Hidden states contain useful residual structure.",
          "They also contain a shared common direction.",
          "Top-1 routing can turn the shared direction into expert-specific offsets."
        ) 68 182 210 132 13 | Out-Null
        Add-Text $slide "Current question" 68 326 210 22 16 $Color.Magenta $true | Out-Null
        Add-Text $slide "Can expert-aware initialization reduce early bias, or does training re-amplify it?" 68 358 210 62 15 $Color.Ink $true | Out-Null
        Add-FigurePanel $slide "s03_storyline_ladder.png" 330 130 570 300 "Seven-day story: from false specialization signal to expert-spectrum stress test"
      }
      "heatmap_false" {
        Add-Header $slide $spec.title $num
        Add-Bullets $slide @(
          "A feature can route consistently while many features still share one expert.",
          "Consistency alone is not evidence of useful specialization.",
          "Track load, assignment structure, and intervention response together."
        ) 58 118 780 74 13 | Out-Null
        Add-ImageContain $slide (Join-Path $Fig "s04_baseline_collapse_heatmaps_cropped.png") 35 210 890 126 | Out-Null
        Add-StatCard $slide "false positive" "same-looking consistency can coexist with collapsed expert usage" 70 366 235 84 $Color.PalePink $Color.Magenta
        Add-StatCard $slide "metric set" "max load + heatmap + intervention, not route consistency alone" 360 366 235 84 (C "#F4F2F5") $Color.Pink
        Add-StatCard $slide "claim" "specialization requires distributed and meaningful expert use" 650 366 235 84 (C "#F4D5E6") $Color.Magenta
      }
      "heatmap_positive" {
        Add-Header $slide $spec.title $num
        Add-Bullets $slide @(
          "Slot-aware initialization produces stable slot-to-expert structure.",
          "Oracle-to-trainable release can preserve specialization after basin entry.",
          "The bottleneck is early basin entry, not impossibility of specialization."
        ) 58 116 790 76 13 | Out-Null
        Add-ImageContain $slide (Join-Path $Fig "s05_slot_init_positive_control_heatmaps_cropped.png") 35 205 890 130 | Out-Null
        Add-FigurePanel $slide "s05_oracle_release_trajectory.png" 600 355 280 110 "release preserves specialization"
        Add-Box $slide 78 360 430 110 $Color.Magenta $null | Out-Null
        Add-Text $slide "Positive control" 100 383 370 25 20 $Color.White $true | Out-Null
        Add-Text $slide "The model can specialize when the early routing basin is controlled." 100 418 370 34 13 $Color.White | Out-Null
      }
      "mechanism" {
        Add-Header $slide $spec.title $num
        Add-Box $slide 52 132 310 260 $Color.PalePink $Color.Line | Out-Null
        Add-Text $slide "Common-logit decomposition" 78 154 250 22 15 $Color.Magenta $true 2 | Out-Null
        Add-ImageContain $slide (Join-Path $Fig "formula_hidden_decomposition.png") 92 188 220 42 | Out-Null
        Add-ImageContain $slide (Join-Path $Fig "formula_gate_score_decomposition.png") 70 242 275 48 | Out-Null
        Add-Text $slide "The common term is shared by tokens but differs across experts; under top-1, it can act like an effective expert bias." 78 316 250 58 14 $Color.Ink | Out-Null
        Add-FigurePanel $slide "s06_common_logit_model.png" 400 126 500 295 "Mechanism candidate: shared input geometry becomes unequal expert scores"
        Add-StatCard $slide "boundary" "routing geometry is not automatically semantic expertise" 72 420 260 62 (C "#F4F2F5") $Color.Pink
        Add-StatCard $slide "target" "audit which geometry is amplified first" 382 420 260 62 (C "#F4D5E6") $Color.Magenta
        Add-Citation $slide "Related claim boundary: Wang et al., The Myth of Expert Specialization in MoEs, 2026."
      }
      "controlled" {
        Add-Header $slide $spec.title $num
        Add-Bullets $slide @(
          "Common margin rises before slot margin becomes decisive.",
          "Common-logit cancellation improves slot NMI while preserving accuracy.",
          "This supports common-logit as intervention-relevant in the controlled setting."
        ) 52 116 820 62 12 | Out-Null
        Add-FigurePanel $slide "s07_common_vs_slot_margin_timing.png" 50 205 390 210 "common margin timing"
        Add-FigurePanel $slide "s07_common_cancellation_metrics.png" 482 205 390 210 "cancellation improves slot structure"
        Add-Box $slide 165 438 640 42 $Color.Magenta $null | Out-Null
        Add-Text $slide "Intervention result: slot NMI improves while accuracy stays at 1.000" 190 451 590 16 13 $Color.White $true 2 | Out-Null
      }
      "realtext" {
        Add-Header $slide $spec.title $num
        Add-Bullets $slide @(
          "After removing top-1% high-frequency tokens, random linear routers still show step-0 load bias.",
          "Centering / common removal reduces the bias, but does not eliminate all structure.",
          "This moves the question from static bias to early training amplification."
        ) 52 116 820 64 12 | Out-Null
        Add-FigurePanel $slide "s09_realtext_step0_common_vs_residual.png" 50 205 390 210 "common vs residual"
        Add-FigurePanel $slide "s09_realtext_raw_vs_centered_load.png" 482 205 390 210 "raw vs centered load"
        Add-StatCard $slide "narrower claim" "common removal helps, but is incomplete on real text" 270 438 420 46 $Color.PalePink $Color.Magenta
      }
      "coupled" {
        Add-Header $slide $spec.title $num
        Add-Bullets $slide @(
          "Freezing only the router or only experts does not explain the full spike.",
          "Freezing the prefix before layer 5 suppresses most early amplification.",
          "Replay shows a large interaction between router updates and hidden-state changes."
        ) 48 112 300 130 13 | Out-Null
        Add-FigurePanel $slide "s11_freeze_split_key_numbers.png" 365 118 250 250 "freeze split"
        Add-FigurePanel $slide "s11_replay_heatmap_common_margin.png" 638 118 250 250 "cross-checkpoint replay"
        Add-Box $slide 76 380 810 64 $Color.Magenta $null | Out-Null
        Add-Text $slide "Update: step-10 route concentration is not gate-only; it is a coupled router-hidden-state amplification." 105 400 750 24 15 $Color.White $true 2 | Out-Null
      }
      "method" {
        Add-Header $slide $spec.title $num
        Add-Bullets $slide @(
          "Expert principal input subspaces are measurable and differ across experts.",
          "Their overlap with the hidden-state common direction is low.",
          "The idea is computationally meaningful, but not yet a specialization claim."
        ) 52 116 820 64 12 | Out-Null
        Add-Pipeline $slide @("Expert input matrices`rgate_proj + up_proj","Principal subspaces`rtop eigen-directions","Common filtering`rremove shared direction","Linear top-1 router`rcurrent bridge") 62 220 835 82
        Add-StatCard $slide "0.0116" "expert-expert subspace overlap" 86 340 235 72 $Color.PaleGray $Color.Magenta
        Add-StatCard $slide "0.0166" "expert-common overlap" 362 340 235 72 $Color.PaleGray $Color.Pink
        Add-StatCard $slide "0.2328" "raw spectrum utility correlation" 638 340 235 72 $Color.PalePink $Color.Magenta
        Add-Citation $slide "Related framing: Ahrac et al., Routers Learn the Geometry of Their Experts, 2026."
      }
      "result" {
        Add-Header $slide $spec.title $num
        Add-Box $slide 52 124 220 300 $Color.PalePink $Color.Line | Out-Null
        Add-Text $slide "Init stress test" 72 150 180 24 17 $Color.Magenta $true | Out-Null
        Add-Text $slide "Step 0 improves after filtering common direction, but step 10 becomes worse than random initialization." 72 192 180 70 13 $Color.Ink | Out-Null
        Add-Text $slide "Main metric: max expert load" 72 290 180 20 13 $Color.Ink $true | Out-Null
        Add-Text $slide "Step 0: 19.98% -> 13.97%" 72 324 180 24 16 $Color.Magenta $true | Out-Null
        Add-Text $slide "Step 10: 83.16% -> 93.51%" 72 356 180 24 16 $Color.Magenta $true | Out-Null
        Add-FigurePanel $slide "s12_0615_spectrum_init_stress_test.png" 305 116 575 332 "better step-0 balance does not stop step-10 amplification"
        Add-Citation $slide "Source: internal meeting brief on expert-spectrum initialization and early route concentration."
      }
      "conclusion" {
        Add-Header $slide $spec.title $num
        Add-FigurePanel $slide "s12_next_mechanism_hypothesis.png" 58 138 300 260 "next mechanism hypothesis"
        Add-ConclusionBar $slide "01" "Expert geometry exists" "Input subspaces differ and are not the common direction." 390 132 500 86 $Color.Pink $Color.White
        Add-ConclusionBar $slide "02" "Step-0 bias can improve" "Common-filtered spectrum reduces initial max load." 390 232 500 86 $Color.Magenta2 $Color.White
        Add-ConclusionBar $slide "03" "Step-10 needs dynamics" "Router-hidden-state amplification dominates initialization alone." 390 332 500 86 $Color.Magenta $Color.White
        Add-Box $slide 58 425 832 54 $Color.PalePink $Color.Line | Out-Null
        Add-Text $slide "Next decision: audit whether step-0 route winners are reinforced by early hidden-state change and router updates; then test a stronger oracle or learned bridge." 82 440 780 20 13 $Color.Magenta $true 2 | Out-Null
      }
      "boundary" {
        Add-Header $slide $spec.title $num
        Add-Box $slide 58 132 410 330 (C "#F1FBF7") (C "#B9DED2") | Out-Null
        Add-Text $slide "Can say" 88 162 340 28 22 $Color.Green $true | Out-Null
        Add-Bullets $slide @(
          "Expert-spectrum directions are measurable and differ across experts.",
          "Common-filtered initialization improves step-0 balance.",
          "Current linear top-1 initialization cannot prevent step-10 concentration."
        ) 88 210 340 170 15 | Out-Null
        Add-Box $slide 494 132 410 330 (C "#FFF7F5") (C "#F1B5AD") | Out-Null
        Add-Text $slide "Cannot say" 524 162 340 28 22 $Color.Red $true | Out-Null
        Add-Bullets $slide @(
          "Expert spectrum is useless.",
          "Domain specialization has been explained.",
          "This generalizes to pretrained large MoEs, top-2/top-4 routing, or load-balancing losses."
        ) 524 210 340 170 15 | Out-Null
      }
      "refs" {
        Add-Header $slide $spec.title $num
        Add-Box $slide 70 130 820 300 $Color.PaleGray $Color.Line | Out-Null
        Add-Text $slide @"
- Shazeer et al., Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer, 2017.
- Fedus et al., Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity, 2021.
- Zoph et al., ST-MoE: Designing Stable and Transferable Sparse Expert Models, 2022.
- Wang et al., The Myth of Expert Specialization in MoEs, 2026.
- Ahrac et al., Routers Learn the Geometry of Their Experts, 2026.
"@ 100 165 760 220 13 $Color.Ink | Out-Null
      }
    }
    if ($Script:Notes.ContainsKey($spec.kind)) {
      Set-Notes $slide $Script:Notes[$spec.kind]
    }
  }

  if (Test-Path $Final) { Remove-Item -LiteralPath $Final -Force }
  $dst.SaveAs($Final, $ppSaveAsOpenXMLPresentation)
  for ($i=1; $i -le $dst.Slides.Count; $i++) {
    $png = Join-Path $Preview ("slide-{0:D2}.png" -f $i)
    $dst.Slides.Item($i).Export($png, "PNG", 1280, 720)
  }
} finally {
  if ($dst) { $dst.Close() }
  if ($src) { $src.Close() }
  if ($ppt) { $ppt.Quit() }
}

Write-Output $Final
