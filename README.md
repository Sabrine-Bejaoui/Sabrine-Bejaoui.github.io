# Sabrine Bejaoui — Portfolio

Personal portfolio of **Sabrine Bejaoui**, second-year Master's student in Decision Support Systems & Data Science (ISG Bizerte, Tunisia), seeking a 6-month end-of-studies internship in Data Science, Machine Learning or AI from February 2027.

**Live site:** https://sabrine-bejaoui.github.io/ · Version française : https://sabrine-bejaoui.github.io/fr/

## Featured projects

- **FraudLens** — financial fraud detection and investigation platform (machine learning on imbalanced data, SHAP explanations).
- **IntelliHire** — NLP recruitment assistant that ranks candidates against job offers with explained scores.
- **KOSU Digital** — real-time productivity monitoring for LEONI's production lines (end-of-studies internship).

## How the site is built

A static, dependency-free site served by GitHub Pages:

- `content.py` holds all text in English and French.
- `build.py` generates the HTML pages (English at the root, French under `/fr/`).
- `assets/` contains the stylesheet, a small script (menu, language switch, image viewer), self-hosted fonts, optimized screenshots (WebP) and the CVs.

To rebuild after editing the content:

```bash
python build.py
```

No API keys or private data are used. FraudLens source code is private; only screenshots and descriptions from its public showcase appear here.

## Credits

Fonts: Newsreader and Instrument Sans (SIL Open Font License).
