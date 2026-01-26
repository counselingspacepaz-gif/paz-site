---
name: HTML構造・アクセシビリティチェック
about: ページ単位でHTML/SEO/アクセシビリティを確認
title: "[HTMLチェック] ページ名を記入"
labels: [checklist, HTML]
assignees: []
---

### 対象ページ
- パス/URL：

### 🔹 基本構造
- [ ] `<!DOCTYPE html>` が宣言されている
- [ ] `<html lang="ja">` が設定されている
- [ ] `<meta charset="UTF-8">` がある
- [ ] `<meta name="viewport">` がある
- [ ] `<title>` が適切に設定されている

### 🔹 SEO・SNS連携
- [ ] `<meta name="description">` が設定されている
- [ ] `<meta property="og:image">` などOGPタグがある
- [ ] `<link rel="canonical">` が設定されている
- [ ] faviconが設定されている

### 🔹 セマンティック構造
- [ ] `<header>`／`<main>`／`<footer>` が使用されている
- [ ] `<section>`／`<article>`／`<nav>` などが適切に使われている

### 🔹 アクセシビリティ
- [ ] 画像に `alt` 属性がある
- [ ] CTAボタンに `aria-label` がある
- [ ] `<noscript>` がある（JS非対応環境への配慮）

### 🔹 予約導線・外部連携
- [ ] 予約リンクが明示的に配置されている
- [ ] SNSアイコンにリンクが設定されている

### 🔹 パフォーマンス
- [ ] `<script>` や `<link>` の読み込み順が適切
