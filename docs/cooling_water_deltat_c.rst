Cooling Water Delta-T (°C)
==================================================

.. raw:: html

   <style>
      :root {
         --charcoal: #1C1D20;
         --business-teal: #004E5A;
         --technical-slate: #2C3E50;
         --tech-accent-hover: #14B8A6;
         --tech-accent-active: #0F766E;
         --container-bg: #FAFAFA;
         --accent-tint: #E6F0F2;
         --system-tint: #F4F6F8;
         --platinum-border: #E1E8ED;
         --slate-bg: #F6F7F9;
         --slate-border: #E1E8ED;
         --slate-muted: #6B7785;
         --success: #004E5A;
         --warning: #F59E0B;
         --danger: #EF4444;
         --info: #3B82F6;
         --matte-olive: #004E5A;
         --matte-teal: #004E5A;
         --developer-lineage: #2C3E50;
         --teal: #004E5A;
         --muted: #6B7785;
         --code-bg: #111827;
      }
      .rst-content > div[role="navigation"],
      .rst-content > h1:first-child,
      .leap-doc-body > section > h1:first-child,
      body > section > h1:first-child { display: none !important; }
      .rst-content, .rst-content p, .rst-content li, .rst-content td {
         color: #0F172A;
         font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
         letter-spacing: -0.01em;
         -webkit-font-smoothing: antialiased;
         -moz-osx-font-smoothing: grayscale;
         text-rendering: optimizeLegibility;
      }
      code, kbd, pre, .font-mono, .highlight pre {
         font-family: "JetBrains Mono", "Fira Code", ui-monospace, SFMono-Regular, Menlo, monospace !important;
         font-size: 12.5px !important;
         letter-spacing: -0.015em !important;
         line-height: 1.6 !important;
         -webkit-font-smoothing: antialiased;
      }
      .leap-page {
         min-height: 100vh;
         background: var(--slate-bg);
         color: var(--charcoal);
         max-width: 100vw;
         overflow-x: hidden;
      }
      .thin-border { border: 1px solid var(--slate-border); }
      .leap-exec-bar {
         width: 100%;
         background: #FFFFFF;
         color: #1C1D20;
         border-bottom: 1px solid #E2E8F0;
      }
      .leap-exec-inner {
         max-width: 1280px;
         margin: 0 auto;
         padding: 12px 24px;
         min-height: 52px;
         display: flex;
         align-items: center;
         justify-content: space-between;
         gap: 18px;
      }
      .leap-logo {
         min-width: 210px;
         width: 210px;
         height: 42px;
         padding: 0;
         display: flex;
         align-items: center;
         justify-content: center;
         background: transparent;
         border-radius: 4px;
      }
      .leap-logo img {
         width: auto;
         max-width: 210px;
         height: 40px;
         display: block;
      }
      .leap-platform-title {
         margin: 0;
         color: #1E293B;
         font-size: 14px;
         font-weight: 600;
         letter-spacing: .05em;
         text-transform: uppercase;
      }
      .leap-platform-subtitle {
         margin: 0;
         color: #64748B;
         font-size: 12px;
      }
      .confidence-dot {
         width: 8px;
         height: 8px;
         background-color: var(--success);
         display: inline-block;
      }
      .growth-badge {
         background-color: #F0FDFA;
         color: var(--success);
         font-size: 11px;
         padding: 2px 6px;
         border: 1px solid #CCFBF1;
      }
      .status-badge {
         background-color: var(--success);
         color: #fff;
         font-size: 11px;
         padding: 2px 8px;
      }
      .status-badge.state-needs-review {
         background: #FFFBEB;
         color: #B45309;
         border: 1px solid #FDE68A;
      }
      .status-badge.state-extracted {
         background: #EFF6FF;
         color: #2563EB;
         border: 1px solid #BFDBFE;
      }
      .status-badge.state-validated {
         background: #F0FDFA;
         color: var(--success);
         border: 1px solid #CCFBF1;
      }
      .status-badge-secondary {
         background: #F8FAFC;
         color: #475569;
         border: 1px solid var(--slate-border);
      }
      .hash-badge {
         background-color: #F8FAFC;
         color: #334155;
         border: 1px solid var(--slate-border);
         font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
         font-size: 10px;
         padding: 4px 8px;
      }
      .subtle-copy {
         min-height: 26px;
         padding: 4px 8px;
         border: 1px solid var(--slate-border);
         background: #fff;
         color: #64748B;
         font-size: 11px;
         font-weight: 500;
      }
      .leap-card-title,
      .section-header {
         margin: 0;
         color: #1E293B;
         font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
         font-size: 13px;
         font-weight: 600;
         letter-spacing: 0.02em;
         text-transform: uppercase;
         line-height: 1.3;
      }
      .leap-main {
         max-width: 1280px;
         margin: 0 auto;
         padding: 32px 24px 40px;
      }
      .dossier-head { margin-bottom: 28px; }
      .dossier-head h2 {
         margin: 0 0 4px;
         color: #0F172A;
         font-size: 26px;
         font-weight: 600;
         letter-spacing: -0.025em;
         text-transform: none;
      }
      .dossier-head p {
         margin: 0;
         color: var(--slate-muted);
         font-size: 14px;
      }
      .dossier-grid {
         display: grid;
         grid-template-columns: minmax(0, 2fr) minmax(320px, 1fr);
         gap: 24px;
      }
      .stack { display: grid; gap: 24px; }
      .right-rail {
         gap: 16px;
         align-content: start;
      }
      .leap-metadata-sidebar {
         display: flex;
         flex-direction: column;
         gap: 20px;
         padding-left: 16px;
      }
      .sidebar-card {
         background: #FFFFFF;
         border: 1px solid var(--slate-border);
         border-radius: 6px;
         padding: 16px;
      }
      .sidebar-card h3 {
         font-size: 11px;
         text-transform: uppercase;
         letter-spacing: 0.05em;
         color: var(--slate-muted);
         margin: 0 0 12px 0;
         font-weight: 600;
      }
      .sidebar-meta-row {
         display: flex;
         justify-content: space-between;
         gap: 14px;
         font-size: 12.5px;
         margin-bottom: 8px;
         line-height: 1.4;
      }
      .sidebar-meta-row:last-child { margin-bottom: 0; }
      .meta-label {
         color: var(--slate-muted);
         flex: 0 0 auto;
      }
      .meta-value {
         color: var(--charcoal);
         font-weight: 500;
         text-align: right;
         min-width: 0;
         overflow-wrap: anywhere;
      }
      .meta-value.code-font {
         font-family: "JetBrains Mono", monospace;
         font-size: 11.5px;
      }
      .sidebar-status-badge {
         display: inline-flex;
         align-items: center;
         gap: 6px;
         font-size: 12px;
         font-weight: 600;
         padding: 4px 8px;
         border-radius: 4px;
         margin-bottom: 12px;
      }
      .status-dot {
         width: 6px;
         height: 6px;
         border-radius: 50%;
         display: inline-block;
      }
      .state-needs-review {
         background: #FFFBEB;
         color: #D97706;
      }
      .state-needs-review .status-dot { background: #D97706; }
      .state-validated {
         background: #F0FDFA;
         color: var(--success);
      }
      .state-validated .status-dot { background: var(--success); }
      .state-extracted {
         background: #EFF6FF;
         color: #2563EB;
      }
      .state-extracted .status-dot { background: #2563EB; }
      .formula-state-pill {
         display: inline-flex;
         align-items: center;
         gap: 6px;
         min-height: 24px;
         padding: 3px 8px;
         border-radius: 4px;
         font-size: 12px;
         font-weight: 600;
      }
      .formula-state-pill.state-needs-review {
         background: #FFFBEB;
         color: #B45309;
         border: 1px solid #FDE68A;
      }
      .formula-state-pill.state-extracted {
         background: #EFF6FF;
         color: #2563EB;
         border: 1px solid #BFDBFE;
      }
      .formula-state-pill.state-validated {
         background: #F0FDFA;
         color: var(--success);
         border: 1px solid #CCFBF1;
      }
      .sidebar-btn {
         display: flex;
         width: 100%;
         min-height: 34px;
         align-items: center;
         justify-content: center;
         padding: 8px 12px;
         font-size: 12px;
         font-weight: 500;
         border-radius: 4px;
         cursor: pointer;
         margin-bottom: 8px;
         border: none;
         font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
         text-decoration: none;
         transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease;
      }
      .sidebar-btn:last-child { margin-bottom: 0; }
      .btn-primary {
         background: var(--charcoal);
         color: #fff;
      }
      .btn-primary:hover,
      .btn-primary:focus-visible {
         background: #2D2F34;
         color: #fff;
      }
      .btn-secondary {
         background: #F1F5F9;
         color: var(--charcoal);
         border: 1px solid var(--slate-border);
      }
      .btn-secondary:hover,
      .btn-secondary:focus-visible {
         background: #E2E8F0;
         color: var(--charcoal);
      }
      .action-card .sidebar-btn {
         justify-content: flex-start;
         min-height: 36px;
         padding: 8px 12px;
         border: 1px solid var(--slate-border);
         border-left: 3px solid transparent;
         border-radius: 4px;
         background: #FFFFFF;
         color: var(--charcoal);
         text-align: left;
      }
      .action-card .sidebar-btn:hover,
      .action-card .sidebar-btn:focus-visible {
         border-left-color: var(--matte-teal);
         background: #FFFFFF;
         color: var(--matte-teal);
         outline: none;
      }
      .sidebar-card.compact-card {
         padding: 14px 16px;
      }
      .review-queue-card {
         scroll-margin-top: 72px;
      }
      .review-queue-card.data-status-alert {
         background-color: #FFF9E6 !important;
         border-left: 4px solid #D97706 !important;
         padding: 16px 20px !important;
         margin-bottom: 24px !important;
      }
      .review-status-header {
         display: flex;
         align-items: center;
         justify-content: space-between;
         gap: 10px;
      }
      .warning-badge {
         display: inline-flex;
         align-items: center;
         gap: 6px;
         min-height: 26px;
         padding: 4px 8px;
         border-radius: 4px;
         background: #FFFBEB;
         color: #B45309;
         font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
         font-size: 12px;
         font-weight: 700;
      }
      .review-message-body p,
      .review-queue-text-display {
         color: #92400E !important;
         font-size: 0.95rem;
         line-height: 1.5;
         margin: 8px 0 0 0;
      }
      .gov-conflict-subpanel {
         margin-top: 10px;
         padding: 10px;
         background-color: #FFF5F5;
         border: 1px solid #FEB2B2;
         border-radius: 6px;
      }
      .gov-conflict-subpanel span {
         display: block;
         color: #9B2C2C;
         font-size: 0.75rem;
         font-weight: 600;
         letter-spacing: 0.04em;
         text-transform: uppercase;
      }
      .gov-conflict-subpanel p {
         margin: 4px 0 0;
         color: #C53030 !important;
         font-size: 0.75rem;
         line-height: 1.35;
      }
      .review-queue-text {
         width: 100%;
         min-height: 150px;
         margin: 10px 0 12px;
         padding: 10px;
         border: 1px solid var(--slate-border);
         background: #F8FAFC;
         color: #334155;
         font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
         font-size: 11px;
         line-height: 1.55;
         resize: vertical;
      }
      .dossier-card {
         background: #fff;
         border: 1px solid var(--slate-border);
         padding: 24px;
         min-width: 0;
      }
      .right-rail .dossier-card {
         padding: 18px 20px;
      }
      .right-rail .leap-card-title,
      .right-rail .section-header {
         margin-bottom: 12px !important;
         font-size: 13px;
      }
      .card-row {
         display: flex;
         align-items: baseline;
         gap: 8px;
         flex-wrap: wrap;
         margin-top: 12px;
      }
      .card-row .label {
         color: var(--slate-muted);
         font-size: 14px;
      }
      .card-row .value {
         color: var(--charcoal);
         font-size: 14px;
         font-weight: 500;
      }
      .formula-panel {
         background: #F8FAFC;
         border: 1px solid var(--slate-border);
         padding: 16px;
         margin: 16px 0;
         max-width: 100%;
         min-width: 0;
         overflow-x: auto;
      }
      .formula-panel .math-equation {
         display: block;
         max-width: 100%;
         overflow-x: auto;
         overflow-y: hidden;
         text-align: center;
         padding: 4px;
         -webkit-overflow-scrolling: touch;
      }
      .formula-panel mjx-container {
         display: block !important;
         width: 100% !important;
         max-width: 100%;
         min-width: 0 !important;
         overflow-x: auto !important;
         overflow-y: hidden;
         padding-bottom: 4px;
      }
      .formula-panel mjx-container[jax="CHTML"][display="true"] {
         display: block !important;
         max-width: 100% !important;
         overflow-x: auto !important;
         overflow-y: hidden !important;
      }
      .formula-panel mjx-container mjx-math {
         max-width: 100% !important;
         min-width: 0 !important;
      }
      .leap-business-formula-math {
         margin: 0 0 16px;
         padding: 18px 16px;
         border: 1px solid #E2E8F0;
         background: #FFFFFF;
         color: #0F172A;
         font-size: 14px;
         line-height: 1.7;
         overflow-x: auto;
      }
      .leap-business-formula-math mjx-container {
         margin: 0 !important;
         max-width: 100%;
         overflow-x: auto;
         overflow-y: hidden;
         font-family: "Latin Modern Math", "STIX Two Math", "Cambria Math", "Times New Roman", serif !important;
         font-size: 112% !important;
      }
      .leap-business-formula-math mjx-container *,
      .formula-panel .math-equation mjx-container * {
         font-family: "Latin Modern Math", "STIX Two Math", "Cambria Math", "Times New Roman", serif !important;
      }
      .leap-business-formula-math mjx-container[jax="CHTML"],
      .formula-panel .math-equation mjx-container[jax="CHTML"] {
         font-family: "Latin Modern Math", "STIX Two Math", "Cambria Math", "Times New Roman", serif !important;
      }
      .leap-business-formula-math mjx-mo,
      .formula-panel .math-equation mjx-mo {
         color: var(--matte-teal) !important;
      }
      .MathJax mtext,
      .MathJax text,
      mjx-mtext,
      mjx-mtext *,
      .leap-business-formula-math mjx-mtext,
      .leap-business-formula-math mjx-mtext *,
      .formula-panel .math-equation mjx-mtext,
      .formula-panel .math-equation mjx-mtext * {
         font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
         font-style: normal !important;
      }
      .leap-code-lineage code,
      .leap-code-lineage pre {
         font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace !important;
      }
      .leap-business-formula-math mjx-mn,
      .formula-panel .math-equation mjx-mn {
         color: #3F5F46 !important;
      }
      .leap-business-formula-math mjx-line,
      .formula-panel .math-equation mjx-line {
         border-color: var(--matte-teal) !important;
      }
      .leap-formula-fallback {
         color: #334155;
      }
      .leap-toggle-container {
         display: inline-flex;
         align-items: center;
         border: 1px solid var(--slate-border);
         padding: 2px;
         background: #fff;
         margin-bottom: 16px;
      }
      .leap-toggle-btn {
         min-height: 28px;
         padding: 4px 12px;
         border: none;
         background: transparent;
         font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
         font-size: 12px;
         color: var(--slate-muted);
         cursor: pointer;
      }
      .leap-toggle-btn.active {
         background: var(--charcoal);
         color: #fff;
         font-weight: 500;
      }
      .leap-toggle-btn:focus-visible {
         outline: 1px solid var(--matte-teal);
         outline-offset: 2px;
      }
      .leap-annotated-equation,
      .leap-annotated-formula-wrapper {
         display: flex;
         align-items: flex-end;
         justify-content: center;
         flex-wrap: wrap;
         gap: 12px 8px;
         max-width: 100%;
         margin: 4px 0 18px;
         padding: 16px 12px;
         border: 1px solid #E2E8F0;
         background: #FFFFFF;
         overflow-x: auto;
      }
      .leap-annotated-equation,
      .leap-annotated-formula-wrapper {
         display: flex !important;
         visibility: visible !important;
         opacity: 1 !important;
         min-height: 2rem !important;
         overflow-x: auto !important;
      }
      .MathJax,
      mjx-container {
         display: block !important;
         visibility: visible !important;
         opacity: 1 !important;
         min-height: 2rem !important;
         overflow-x: auto !important;
      }
      .leap-formula-node {
         display: flex;
         flex-direction: column;
         align-items: center;
         position: relative;
         min-width: 72px;
         max-width: 190px;
         padding: 0 16px;
         opacity: 0.70;
         cursor: pointer;
         transition: opacity 0.25s cubic-bezier(0.4, 0, 0.2, 1), transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
      }
      .operator-node .leap-math-lbl {
         background: #FFFFFF;
      }
      .operator-node .leap-math-render {
         color: #64748B;
      }
      .leap-formula-node:hover,
      .leap-formula-node:focus-within {
         opacity: 1;
         transform: translateY(-2px);
      }
      .leap-math-lbl {
         display: inline-flex;
         align-items: center;
         justify-content: center;
         max-width: 190px;
         min-height: 26px;
         padding: 4px 10px;
         border: 1px solid #E2E8F0;
         border-radius: 4px;
         background: #F1F5F9;
         color: var(--muted);
         font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
         font-size: 11px;
         font-weight: 500;
         line-height: 1.25;
         text-align: center;
         white-space: nowrap;
         overflow-wrap: anywhere;
         transition: all 0.2s ease;
      }
      .leap-math-lbl.long-line {
         white-space: normal;
      }
      .leap-math-pointer {
         width: 1px;
         height: 20px;
         border-left: 1px dashed #94A3B8;
         margin: 6px 0;
         position: relative;
         transition: border-left 0.2s ease;
      }
      .leap-math-pointer::after {
         content: "";
         position: absolute;
         bottom: 0;
         left: -2px;
         width: 3px;
         height: 3px;
         background-color: #94A3B8;
         border-radius: 50%;
         transition: background-color 0.2s ease, transform 0.2s ease;
      }
      .leap-math-render {
         display: inline-flex;
         align-items: center;
         justify-content: center;
         min-height: 28px;
         padding-top: 4px;
         color: var(--charcoal);
         font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
         font-size: 17px;
         font-weight: 400;
         line-height: 1.2;
         text-align: center;
         overflow-wrap: anywhere;
         transition: color 0.2s ease, transform 0.2s ease;
      }
      .leap-formula-node:hover .leap-math-lbl,
      .leap-formula-node:focus-within .leap-math-lbl {
         border-color: var(--teal);
         background: var(--teal);
         color: #FFFFFF;
      }
      .leap-formula-node:hover .leap-math-pointer,
      .leap-formula-node:focus-within .leap-math-pointer {
         border-left: 1px solid var(--teal);
      }
      .leap-formula-node:hover .leap-math-pointer::after,
      .leap-formula-node:focus-within .leap-math-pointer::after {
         background-color: var(--teal);
         transform: scale(1.4);
      }
      .leap-formula-node:hover .leap-math-render,
      .leap-formula-node:focus-within .leap-math-render {
         color: var(--teal);
         transform: translateY(1px);
      }
      .leap-eq-operator {
         min-width: 18px;
         padding-bottom: 10px;
         color: #64748B;
         font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
         font-size: 18px;
         line-height: 1;
         text-align: center;
      }
      .leap-annotated-equation[data-perspective="developer"] .leap-math-lbl {
         background: #FFFFFF;
         color: var(--slate-muted);
         font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
         font-size: 10.5px;
         letter-spacing: -0.015em;
      }
      .leap-annotated-equation[data-perspective="developer"] .leap-math-pointer {
         border-left-color: var(--slate-muted);
      }
      .leap-annotated-equation[data-perspective="developer"] .leap-math-pointer::after {
         background-color: var(--slate-muted);
      }
      .leap-annotated-equation[data-perspective="developer"] .leap-formula-node:hover .leap-math-lbl,
      .leap-annotated-equation[data-perspective="developer"] .leap-formula-node:focus-within .leap-math-lbl {
         border-color: var(--developer-lineage);
         background: var(--developer-lineage);
         color: #FFFFFF;
      }
      .leap-annotated-equation[data-perspective="developer"] .leap-formula-node:hover .leap-math-pointer,
      .leap-annotated-equation[data-perspective="developer"] .leap-formula-node:focus-within .leap-math-pointer {
         border-left-color: var(--developer-lineage);
      }
      .leap-annotated-equation[data-perspective="developer"] .leap-formula-node:hover .leap-math-pointer::after,
      .leap-annotated-equation[data-perspective="developer"] .leap-formula-node:focus-within .leap-math-pointer::after {
         background-color: var(--developer-lineage);
      }
      .leap-annotated-equation[data-perspective="developer"] .leap-formula-node:hover .leap-math-render,
      .leap-annotated-equation[data-perspective="developer"] .leap-formula-node:focus-within .leap-math-render {
         color: var(--developer-lineage);
      }
      .leap-code-lineage {
         margin: -4px 0 18px;
         border: 1px solid #E2E8F0;
         background: #FFFFFF;
      }
      .leap-code-lineage-title {
         padding: 10px 12px;
         border-bottom: 1px solid #E2E8F0;
         background: #F8FAFC;
         color: #334155;
         font-size: 11px;
         font-weight: 600;
         letter-spacing: .05em;
         text-transform: uppercase;
      }
      .leap-code-lineage-row {
         display: grid;
         grid-template-columns: minmax(0, 1.05fr) minmax(0, 1fr);
         gap: 12px;
         padding: 10px 12px;
         border-bottom: 1px solid #F1F5F9;
      }
      .leap-code-lineage-row:last-child {
         border-bottom: 0;
      }
      .leap-code-lineage-code {
         color: #0F172A;
         font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
         font-size: 11px;
         line-height: 1.45;
         overflow-wrap: anywhere;
      }
      .leap-code-lineage-role {
         color: #64748B;
         font-size: 12px;
         line-height: 1.45;
      }
      .leap-code-lineage,
      .leap-code-lineage pre,
      #source-evidence pre,
      .highlight,
      div[id^="source-evidence"] pre,
      .highlight pre,
      .highlight-python pre,
      .highlight-javascript pre,
      .highlight-sql pre,
      .highlight-text pre {
         background-color: #1E1E2E !important;
         color: #CDD6F4 !important;
         font-family: "JetBrains Mono", "Courier New", monospace !important;
         font-size: 0.92rem !important;
         line-height: 1.6 !important;
         border: 1px solid #2C3E50 !important;
         border-radius: 8px !important;
         padding: 18px !important;
         box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
         overflow-x: auto !important;
      }
      .leap-code-lineage {
         background-color: #181825 !important;
         border: 1px solid #004E5A !important;
         border-radius: 8px !important;
         padding: 20px !important;
         margin-top: 15px !important;
      }
      .leap-code-lineage-code,
      .leap-code-lineage-code *,
      .leap-code-lineage-role,
      .leap-code-lineage-row,
      .leap-code-lineage table,
      .leap-code-lineage td,
      .leap-code-lineage th {
         color: #CDD6F4 !important;
         font-family: "JetBrains Mono", "Courier New", monospace !important;
      }
      .leap-code-lineage-title {
         color: #89B4FA !important;
         background: transparent !important;
         border: none !important;
      }
      .leap-code-lineage th {
         color: #89B4FA !important;
         border-bottom: 2px solid #313244 !important;
      }
      .leap-code-lineage-row {
         border-bottom: 1px solid #313244 !important;
      }
      .leap-code-lineage pre::-webkit-scrollbar,
      div[id^="source-evidence"] pre::-webkit-scrollbar {
         height: 6px;
      }
      .leap-code-lineage pre::-webkit-scrollbar-thumb,
      div[id^="source-evidence"] pre::-webkit-scrollbar-thumb {
         background: #45475a;
         border-radius: 4px;
      }
      .highlight .k { color: #cba6f7 !important; font-weight: 600; }
      .highlight .nf { color: #89b4fa !important; }
      .highlight .nn { color: #f9e2af !important; }
      .highlight .s2,
      .highlight .s1 { color: #a6e3a1 !important; }
      .highlight .mi,
      .highlight .mf { color: #fab387 !important; }
      .highlight .c1 { color: #6c7086 !important; font-style: italic !important; }
      #source-evidence .highlight .k { color: #CBA6F7 !important; font-weight: 700 !important; }
      #source-evidence .highlight .mi,
      #source-evidence .highlight .mf { color: #FAB387 !important; }
      .semantic-grid {
         display: grid;
         grid-template-columns: repeat(2, minmax(0, 1fr));
         gap: 14px;
      }
      .semantic-item {
         border-top: 1px solid var(--slate-border);
         padding-top: 12px;
      }
      .semantic-item:first-child,
      .semantic-item:nth-child(2) {
         border-top: 0;
         padding-top: 0;
      }
      .micro-label {
         color: var(--slate-muted);
         font-size: 11px;
         font-weight: 600;
         letter-spacing: .04em;
         text-transform: uppercase;
         margin-bottom: 5px;
      }
      .literate-step {
         display: grid;
         grid-template-columns: 140px 1fr;
         gap: 16px;
         padding: 14px 0;
         border-top: 1px solid var(--slate-border);
      }
      .literate-step:first-of-type { border-top: 0; padding-top: 0; }
      .literate-step ol {
         margin: 0;
         padding-left: 18px;
      }
      .literate-step li {
         margin: 0 0 8px;
      }
      .walkthrough-proof-list {
         display: grid;
         gap: 8px;
      }
      .walkthrough-proof-item {
         display: grid;
         grid-template-columns: 24px 1fr;
         gap: 8px;
         align-items: start;
         padding: 10px;
         border: 1px solid #E2E8F0;
         background: #F8FAFC;
      }
      .walkthrough-check {
         display: inline-flex;
         align-items: center;
         justify-content: center;
         width: 18px;
         height: 18px;
         background: #F0FDFA;
         color: var(--matte-teal);
         border: 1px solid #99F6E4;
         font-size: 11px;
         line-height: 1;
      }
      .walkthrough-heading {
         display: flex;
         align-items: center;
         justify-content: space-between;
         gap: 12px;
         margin-bottom: 16px;
      }
      .framework-seal {
         width: 38px;
         height: 38px;
         flex: 0 0 auto;
         border: 1px solid var(--slate-border);
         background: #fff;
         padding: 6px;
      }
      .framework-seal img {
         width: 100%;
         height: 100%;
         display: block;
      }
      .evidence-inline {
         margin-top: 14px;
         border: 1px solid #1F2937;
         background: var(--code-bg);
      }
      .evidence-inline summary {
         cursor: pointer;
         color: #F8FAFC;
         padding: 10px 12px;
         font-size: 12px;
         font-weight: 500;
         list-style: none;
      }
      .evidence-inline summary::-webkit-details-marker { display:none; }
      .evidence-inline summary:focus-visible {
         outline: 1px solid var(--matte-teal);
         outline-offset: 2px;
      }
      .evidence-inline pre {
         margin: 0;
         padding: 12px;
         overflow-x: auto;
         border-top: 1px solid #1F2937;
         color: #D1D5DB;
         background: var(--code-bg);
      }
      .dependency-row {
         display: flex;
         align-items: flex-start;
         gap: 12px;
         padding: 10px 0;
         border-bottom: 1px solid var(--slate-border);
      }
      .dependency-row:last-child { border-bottom: 0; }
      .tiny-dot {
         width: 4px;
         height: 4px;
         margin-top: 9px;
         background: var(--success);
         flex: 0 0 auto;
      }
      .source-chip {
         color: var(--info);
         font-size: 12px;
         font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
      }
      .right-row {
         display: flex;
         align-items: center;
         justify-content: space-between;
         gap: 12px;
         padding: 8px 0;
         font-size: 14px;
      }
      .right-row span:first-child { color: var(--slate-muted); }
      .right-rail .right-row {
         min-height: 30px;
         padding: 6px 0;
         font-size: 13px;
      }
      .right-rail .right-row strong {
         max-width: 58%;
         text-align: right;
      }
      .right-rail .hash-badge {
         min-height: 26px;
         display: flex;
         align-items: center;
      }
      .right-rail .raci-grid {
         gap: 6px;
      }
      .right-rail .raci-key,
      .right-rail .raci-value {
         padding: 7px 9px;
      }
      .state-divider {
         border-top: 1px solid var(--slate-border);
         margin-top: 12px;
         padding-top: 12px;
      }
      .raci-grid {
         display: grid;
         grid-template-columns: 44px 1fr;
         gap: 8px;
         font-size: 12px;
      }
      .raci-key {
         display: inline-flex;
         align-items: center;
         justify-content: center;
         width: 22px;
         height: 22px;
         padding: 0;
         margin-right: 6px;
         border-radius: 4px;
         text-align: center;
         font-size: 11px;
         font-weight: 700;
      }
      .raci-value {
         padding: 8px 10px;
         border: 1px solid var(--slate-border);
      }
      .raci-badge { display: inline-flex; align-items: center; justify-content: center; width: 22px; height: 22px; font-weight: 700; font-size: 11px; border-radius: 4px; margin-right: 6px; }
      .raci-r { background: #0D9488; color: #FFFFFF; }
      .raci-a { background: #1C1D20; color: #FFFFFF; }
      .raci-c { background: #E2E8F0; color: #475569; border: 1px solid #CBD5E1; }
      .raci-i { background: #F1F5F9; color: #64748B; }
      .action-row {
         display: flex;
         flex-wrap: wrap;
         gap: 8px;
         margin-top: 16px;
      }
      .action-btn {
         display: inline-flex;
         align-items: center;
         min-height: 32px;
         padding: 7px 10px;
         border: 1px solid var(--slate-border);
         border-left: 3px solid transparent;
         background: #fff;
         color: var(--charcoal) !important;
         text-decoration: none;
         font-size: 12px;
         font-weight: 500;
         transition: border-color 0.15s ease, color 0.15s ease, background 0.15s ease;
      }
      .action-btn-primary {
         background: #fff;
         border-color: var(--slate-border);
         border-left-color: transparent;
         color: var(--charcoal) !important;
      }
      .action-btn:hover,
      .action-btn:focus-visible,
      .action-btn-primary:hover,
      .action-btn-primary:focus-visible {
         border-left-color: var(--matte-teal);
         background: #fff;
         color: var(--matte-teal) !important;
         outline: none;
      }
      .leap-footer-shell {
         margin-top: 28px;
         background: var(--slate-bg);
         border-top: 1px solid var(--slate-border);
      }
      .leap-footer {
         max-width: 1440px;
         margin: 0 auto;
         padding: 24px;
         display: flex;
         align-items: center;
         justify-content: space-between;
         gap: 16px;
         flex-wrap: wrap;
         color: var(--slate-muted);
         font-size: 12px;
      }
      .leap-footer-links {
         display: flex;
         align-items: center;
         gap: 24px;
         flex-wrap: wrap;
      }
      .leap-footer a {
         color: var(--slate-muted);
         text-decoration: none;
      }
      .leap-footer a:hover {
         color: var(--success);
      }
      .highlight,
      .highlight pre {
         background: #1e1e2e !important;
         color: #cdd6f4 !important;
      }
      .highlight {
         border: none !important;
         border-radius: 8px !important;
         overflow-x: auto;
      }
      .highlight pre {
         padding: 18px 24px !important;
         font-size: 0.92rem !important;
         line-height: 1.6 !important;
      }
      .headerlink {
         display: none !important;
      }
      .source-code-dropdown {
         margin: 0;
         background: transparent;
         border: none;
         color: #D1D5DB;
      }
      .leap-source-wrap {
         max-width: 1280px;
         margin: 0 auto;
         padding: 0 24px 32px;
      }
      .source-code-dropdown summary {
         padding: 14px 16px;
         color: #fff;
         cursor: pointer;
         font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
         font-size: 14px;
         font-weight: 500;
         list-style: none;
      }
      .source-code-dropdown summary::-webkit-details-marker {
         display: none;
      }
      .source-code-dropdown summary:focus-visible {
         outline: 1px solid var(--matte-teal);
         outline-offset: 2px;
      }
      .source-code-dropdown summary::before {
         content: "+";
         display: inline-block;
         width: 16px;
         color: var(--success);
         font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
      }
      .source-code-dropdown[open] summary::before {
         content: "-";
      }
      .source-code-dropdown .highlight {
         border: 0;
         border-top: 0;
         margin: 0;
      }
      /* LEAP Executive Color Strategy: Deep Teal & Technical Slate */
      .leap-doc-primary,
      .leap-metric-card,
      .leap-side-card,
      .dossier-card,
      .formula-panel,
      .sidebar-card,
      .review-queue-card,
      .semantic-item,
      .literate-step,
      .leap-annotated-equation,
      .leap-annotated-formula-wrapper {
         background-color: var(--container-bg) !important;
         border-color: var(--platinum-border) !important;
      }
      .business-reading-card {
         box-shadow: inset 3px 0 0 var(--business-teal) !important;
      }
      .business-reading-card .leap-card-title,
      .business-reading-card .micro-label,
      .formula-panel > .micro-label,
      .leap-business-formula-math,
      .leap-business-formula-math mjx-container,
      .leap-business-formula-math mjx-mo,
      .formula-panel .math-equation mjx-mo {
         color: var(--business-teal) !important;
      }
      .business-reading-card .semantic-item,
      .business-reading-card .literate-step {
         background: #FFFFFF !important;
      }
      .system-identifier-card,
      .system-card,
      .source-card {
         background-color: var(--system-tint) !important;
      }
      .system-identifier-card {
         border-color: var(--platinum-border) !important;
         box-shadow: inset 3px 0 0 var(--technical-slate) !important;
      }
      .system-identifier-card .leap-card-title,
      .system-identifier-card .label,
      .system-identifier-card .value,
      .system-identifier-card .font-mono,
      .source-card .meta-value,
      .meta-value.code-font,
      .hash-badge {
         color: var(--technical-slate) !important;
      }
      .leap-toggle-container {
         background: #FFFFFF !important;
         border-color: var(--platinum-border) !important;
         border-radius: 6px !important;
      }
      .leap-toggle-btn {
         color: var(--text-muted, #64748B) !important;
         border-radius: 4px !important;
      }
      .leap-toggle-btn[data-perspective="business"].active {
         background-color: var(--accent-tint) !important;
         color: var(--business-teal) !important;
         box-shadow: inset 0 0 0 1px rgba(0, 78, 90, 0.18) !important;
      }
      .leap-toggle-btn[data-perspective="developer"].active {
         background-color: var(--tech-accent-active) !important;
         color: #FFFFFF !important;
         border-color: var(--tech-accent-active) !important;
         box-shadow: 0 2px 4px rgba(20, 184, 166, 0.18) !important;
      }
      .leap-toggle-btn[data-perspective="developer"]:hover,
      .leap-toggle-btn[data-perspective="developer"]:focus-visible {
         background-color: var(--tech-accent-hover) !important;
         color: #FFFFFF !important;
         border-color: var(--tech-accent-hover) !important;
         box-shadow: 0 2px 4px rgba(20, 184, 166, 0.2) !important;
      }
      .leap-math-lbl {
         background: var(--accent-tint) !important;
         border-color: var(--platinum-border) !important;
         color: var(--business-teal) !important;
      }
      .leap-math-pointer {
         border-left-color: rgba(0, 78, 90, 0.42) !important;
      }
      .leap-math-pointer::after {
         background-color: var(--business-teal) !important;
      }
      .leap-formula-node:hover .leap-math-lbl,
      .leap-formula-node:focus-within .leap-math-lbl {
         background: var(--business-teal) !important;
         border-color: var(--business-teal) !important;
         color: #FFFFFF !important;
      }
      .leap-formula-node:hover .leap-math-pointer,
      .leap-formula-node:focus-within .leap-math-pointer {
         border-left-color: var(--business-teal) !important;
      }
      .leap-formula-node:hover .leap-math-render,
      .leap-formula-node:focus-within .leap-math-render {
         color: var(--business-teal) !important;
      }
      .leap-annotated-equation[data-perspective="developer"] {
         background: var(--system-tint) !important;
      }
      .leap-annotated-equation[data-perspective="developer"] .leap-math-lbl {
         background: #FFFFFF !important;
         border-color: var(--platinum-border) !important;
         color: var(--technical-slate) !important;
      }
      .leap-annotated-equation[data-perspective="developer"] .leap-math-pointer {
         border-left-color: rgba(44, 62, 80, 0.45) !important;
      }
      .leap-annotated-equation[data-perspective="developer"] .leap-math-pointer::after {
         background-color: var(--technical-slate) !important;
      }
      .leap-annotated-equation[data-perspective="developer"] .leap-formula-node:hover .leap-math-lbl,
      .leap-annotated-equation[data-perspective="developer"] .leap-formula-node:focus-within .leap-math-lbl {
         background: var(--technical-slate) !important;
         border-color: var(--technical-slate) !important;
         color: #FFFFFF !important;
      }
      .leap-annotated-equation[data-perspective="developer"] .leap-formula-node:hover .leap-math-pointer,
      .leap-annotated-equation[data-perspective="developer"] .leap-formula-node:focus-within .leap-math-pointer {
         border-left-color: var(--technical-slate) !important;
      }
      .leap-annotated-equation[data-perspective="developer"] .leap-formula-node:hover .leap-math-render,
      .leap-annotated-equation[data-perspective="developer"] .leap-formula-node:focus-within .leap-math-render {
         color: var(--technical-slate) !important;
      }
      .leap-business-formula-math,
      .leap-annotated-equation,
      .leap-annotated-formula-wrapper,
      mjx-container[display="true"] {
         display: flex !important;
         justify-content: center !important;
         align-items: center !important;
         text-align: center !important;
         margin: 25px auto !important;
         font-size: 1.25rem !important;
         width: 100% !important;
      }
      #source-evidence pre,
      #source-evidence .highlight,
      #source-evidence .highlight pre,
      .source-code-dropdown,
      .source-code-dropdown .highlight,
      .source-code-dropdown .highlight pre,
      div[id^="source-evidence"] pre {
         background-color: #1E1E2E !important;
         color: #CDD6F4 !important;
         font-family: "JetBrains Mono", monospace !important;
         padding: 18px !important;
         border-radius: 8px !important;
         border: 1px solid #2C3E50 !important;
         overflow-x: auto !important;
      }
      .leap-code-lineage {
         background-color: #181825 !important;
         border: 1px solid var(--business-teal) !important;
         border-radius: 8px !important;
         padding: 20px !important;
         margin-top: 15px !important;
      }
      .leap-code-lineage-row,
      .leap-code-lineage-code,
      .leap-code-lineage-code *,
      .leap-code-lineage-role,
      .leap-code-lineage table,
      .leap-code-lineage td,
      .leap-code-lineage th {
         color: #CDD6F4 !important;
         font-family: "JetBrains Mono", monospace !important;
      }
      .leap-code-lineage th,
      .leap-code-lineage-title {
         color: #89B4FA !important;
         border-bottom-color: #313244 !important;
      }
      .action-btn:hover,
      .action-btn:focus-visible,
      .action-btn-primary:hover,
      .action-btn-primary:focus-visible,
      .leap-footer a:hover {
         border-left-color: var(--business-teal) !important;
         color: var(--business-teal) !important;
      }
      .sidebar-btn:hover,
      .sidebar-btn:focus-visible,
      #open-email-draft-btn:hover,
      #open-email-draft-btn:focus-visible {
         background-color: var(--business-teal) !important;
         color: #FFFFFF !important;
      }
      .raci-r {
         background: var(--business-teal) !important;
      }
      .source-chip,
      .growth-badge,
      .state-validated,
      .status-badge.state-validated {
         color: var(--business-teal) !important;
         background-color: var(--accent-tint) !important;
         border-color: rgba(0, 78, 90, 0.18) !important;
      }
      .leap-precision-divider,
      hr.leap-precision-divider {
         display: block !important;
         border: 0 !important;
         height: 1px !important;
         background: linear-gradient(to right, rgba(225, 232, 237, 0.1), rgba(0, 78, 90, 0.4) 15%, rgba(0, 78, 90, 0.4) 85%, rgba(225, 232, 237, 0.1)) !important;
         margin: 45px auto 25px auto !important;
         padding: 0 !important;
         max-width: 1280px;
      }
      /* DIRECTOR'S DIRECTIVE: ABSOLUTE SHARP CORNER ERADICATION */
      .leap-code-lineage,
      .leap-source-evidence,
      div[id^="source-evidence"],
      section[id^="source-evidence"],
      section#source-evidence,
      div[class^="highlight"],
      .highlight,
      .highlight pre,
      div[class^="highlight"] pre,
      .leap-code-lineage pre,
      .code-panel pre {
         border-radius: 8px !important;
         overflow: hidden !important;
      }
      .highlight pre code,
      div[class^="highlight"] pre code,
      .leap-code-lineage pre code {
         border-radius: 6px !important;
      }
      .sidebar-card,
      .leap-nav-card,
      .review-queue-card,
      .formula-panel,
      .data-status-alert {
         border-radius: 8px !important;
         overflow: hidden !important;
      }
      .sidebar-btn,
      .leap-toggle-btn {
         border-radius: 4px !important;
      }
      /* Portable enforcement sweep for smooth, border-flattened evidence blocks */
      .leap-source-evidence,
      .evidence-inline,
      div[id^="source-evidence"],
      section[id^="source-evidence"],
      section#source-evidence,
      .source-code-dropdown,
      .leap-code-lineage,
      div[class^="highlight"],
      .highlight {
         border-radius: 8px !important;
         overflow: hidden !important;
         border: 1px solid #2C3E50 !important;
         background-color: #1E1E2E !important;
         padding: 0 !important;
         margin-bottom: 1.5rem !important;
      }
      div[class^="highlight"] pre,
      .highlight pre,
      .leap-code-lineage pre,
      .code-panel pre,
      .evidence-inline pre,
      #source-evidence pre,
      .source-code-dropdown pre {
         border: none !important;
         background-color: transparent !important;
         margin: 0 !important;
         padding: 18px !important;
         border-radius: 0 !important;
         box-shadow: none !important;
      }
      div[class^="highlight"] pre code,
      .highlight pre code,
      .leap-code-lineage pre code,
      #source-evidence pre code,
      .source-code-dropdown pre code {
         background: transparent !important;
         border: none !important;
         padding: 0 !important;
         border-radius: 0 !important;
      }
      section#source-evidence .source-code-dropdown,
      section#source-evidence div[class^="highlight"],
      section#source-evidence .highlight,
      .source-code-dropdown div[class^="highlight"],
      .source-code-dropdown .highlight,
      .evidence-inline pre {
         border: none !important;
         border-radius: 0 !important;
         background-color: transparent !important;
         margin: 0 !important;
         box-shadow: none !important;
      }
      /* Figma-style section headers: clear anchors without boxed title fatigue. */
      .leap-doc-primary section > h2,
      .leap-doc-primary section > h3,
      .rst-content section > h2,
      .rst-content section > h3 {
         position: relative !important;
         padding-bottom: 10px !important;
         margin-top: 2.5rem !important;
         margin-bottom: 1.5rem !important;
         color: #2D3748 !important;
         font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
         font-size: 14px !important;
         font-weight: 600 !important;
         letter-spacing: 0.05em !important;
         text-transform: uppercase !important;
         border-bottom: 1px solid #E2E8F0 !important;
      }
      .leap-doc-primary section > h2::after,
      .leap-doc-primary section > h3::after,
      .rst-content section > h2::after,
      .rst-content section > h3::after {
         content: "" !important;
         position: absolute !important;
         bottom: -1px !important;
         left: 0 !important;
         width: 60px !important;
         height: 3px !important;
         background-color: #4A5568 !important;
         border-radius: 2px !important;
      }
      .dossier-card > .leap-card-title,
      .walkthrough-heading > .leap-card-title {
         position: relative !important;
         display: block !important;
         width: 100% !important;
         padding-bottom: 10px !important;
         margin-top: 0 !important;
         margin-bottom: 18px !important;
         color: #2D3748 !important;
         border-bottom: 1px solid #E2E8F0 !important;
      }
      .dossier-card > .leap-card-title::after,
      .walkthrough-heading > .leap-card-title::after {
         content: "" !important;
         position: absolute !important;
         bottom: -1px !important;
         left: 0 !important;
         width: 60px !important;
         height: 3px !important;
         background-color: #4A5568 !important;
         border-radius: 2px !important;
      }
      .business-reading-card > .leap-card-title::after,
      .formula-panel .leap-card-title::after {
         background-color: var(--business-teal) !important;
      }
      .system-identifier-card > .leap-card-title::after,
      .source-card h3::after {
         background-color: var(--technical-slate) !important;
      }
      .sidebar-card h3 {
         position: relative !important;
         padding-bottom: 9px !important;
         margin: 0 0 14px 0 !important;
         color: #2D3748 !important;
         border-bottom: 1px solid #E2E8F0 !important;
      }
      .sidebar-card h3::after {
         content: "" !important;
         position: absolute !important;
         bottom: -1px !important;
         left: 0 !important;
         width: 42px !important;
         height: 2px !important;
         background-color: var(--tech-accent-active) !important;
         border-radius: 2px !important;
      }
      /* FINAL INLINE OVERRIDE: one-shell evidence consoles, no nested borders */
      .leap-source-evidence,
      .evidence-inline,
      div[id^="source-evidence"],
      section[id^="source-evidence"],
      section#source-evidence,
      .source-code-dropdown,
      .leap-code-lineage,
      div[class^="highlight"],
      .highlight {
         border-radius: 8px !important;
         overflow: hidden !important;
         border: 1px solid #2C3E50 !important;
         background-color: #1E1E2E !important;
         padding: 0 !important;
         margin-bottom: 1.5rem !important;
      }
      section#source-evidence .source-code-dropdown,
      section#source-evidence div[class^="highlight"],
      section#source-evidence .highlight,
      .source-code-dropdown div[class^="highlight"],
      .source-code-dropdown .highlight {
         border: none !important;
         border-radius: 0 !important;
         background-color: transparent !important;
         margin: 0 !important;
         padding: 0 !important;
         box-shadow: none !important;
      }
      div[class^="highlight"] pre,
      .highlight pre,
      .leap-code-lineage pre,
      .code-panel pre,
      .evidence-inline pre,
      #source-evidence pre,
      #source-evidence .highlight pre,
      #source-evidence div[class^="highlight"] pre,
      section#source-evidence .highlight pre,
      section#source-evidence div[class^="highlight"] pre,
      .source-code-dropdown pre {
         border: 0 !important;
         border-width: 0 !important;
         border-style: none !important;
         background-color: transparent !important;
         margin: 0 !important;
         padding: 18px !important;
         border-radius: 0 !important;
         box-shadow: none !important;
      }
      div[class^="highlight"] pre code,
      .highlight pre code,
      .leap-code-lineage pre code,
      #source-evidence pre code,
      .source-code-dropdown pre code {
         background: transparent !important;
         border: none !important;
         padding: 0 !important;
         border-radius: 0 !important;
      }
      /* LEAP AXIS DESIGN CORE: absolute smoothing and nesting elimination */
      .leap-source-evidence,
      div[id^="source-evidence"],
      section[id^="source-evidence"],
      section#source-evidence,
      .source-code-dropdown,
      .leap-code-lineage,
      div[class^="highlight"],
      .highlight {
         border-radius: 8px !important;
         overflow: hidden !important;
         border: 1px solid #2C3E50 !important;
         background-color: #1E1E2E !important;
         padding: 0 !important;
         box-sizing: border-box;
      }
      section#source-evidence .source-code-dropdown,
      section#source-evidence div[class^="highlight"],
      section#source-evidence .highlight,
      .source-code-dropdown div[class^="highlight"],
      .source-code-dropdown .highlight {
         border: none !important;
         background-color: transparent !important;
         border-radius: 0 !important;
         margin: 0 !important;
         padding: 0 !important;
         box-shadow: none !important;
      }
      div[class^="highlight"] pre,
      .highlight pre,
      .leap-code-lineage pre,
      .code-panel pre,
      .evidence-inline pre,
      #source-evidence pre,
      #source-evidence .highlight pre,
      #source-evidence div[class^="highlight"] pre,
      section#source-evidence .highlight pre,
      section#source-evidence div[class^="highlight"] pre,
      .source-code-dropdown pre {
         border: none !important;
         background-color: transparent !important;
         margin: 0 !important;
         padding: 18px !important;
         border-radius: 0 !important;
         box-shadow: none !important;
      }
      div[class^="highlight"] pre code,
      .highlight pre code,
      .leap-code-lineage pre code,
      #source-evidence pre code,
      .source-code-dropdown pre code {
         background: transparent !important;
         border: none !important;
         padding: 0 !important;
         border-radius: 0 !important;
      }
      section h2,
      .section h2 {
         position: relative;
         padding-bottom: 12px;
         margin-top: 2.8rem;
         margin-bottom: 1.6rem;
         color: #2C3E50;
         font-weight: 600;
         letter-spacing: 0.05em;
         text-transform: uppercase;
         border-bottom: 1px solid #E2E8F0;
      }
      section h2::after,
      .section h2::after {
         content: "";
         position: absolute;
         bottom: -1px;
         left: 0;
         width: 60px;
         height: 3px;
         background-color: #004E5A;
         border-radius: 2px;
      }
      /* Keep executive/cards light. Only code and source evidence use the dark console shell above. */
      .sidebar-card,
      .leap-nav-card,
      .formula-panel,
      .review-queue-card {
         background-color: #FFFFFF !important;
         color: var(--charcoal) !important;
         border: 1px solid var(--platinum-border) !important;
         border-radius: 8px !important;
         overflow: hidden !important;
      }
      .formula-panel {
         background-color: var(--container-bg) !important;
      }
      .sidebar-card h3,
      .formula-panel .leap-card-title,
      .review-queue-card h3,
      .sidebar-card .meta-value,
      .sidebar-card .meta-label,
      .formula-panel .micro-label {
         color: inherit !important;
      }
      .sidebar-card h3,
      .sidebar-card .meta-label,
      .formula-panel .micro-label {
         color: var(--slate-muted) !important;
      }
      .sidebar-card .meta-value,
      .formula-panel .leap-card-title {
         color: #1E293B !important;
      }
      .data-status-alert,
      .review-queue-card.data-status-alert {
         background-color: #FFF9E6 !important;
         color: #92400E !important;
         border: 1px solid #FDE68A !important;
         border-left: 4px solid #D97706 !important;
         border-radius: 8px !important;
         overflow: hidden !important;
      }
      .sidebar-card h3::after,
      .formula-panel .leap-card-title::after {
         background-color: #004E5A !important;
      }
      @media (max-width: 900px) {
         html, body { max-width: 100%; overflow-x: hidden; }
         .leap-exec-inner { align-items: flex-start; flex-direction: column; padding-top: 12px; padding-bottom: 12px; }
         .dossier-grid { grid-template-columns: 1fr; }
         .leap-main { padding-left: 16px; padding-right: 16px; }
         .dossier-card { padding: 18px; }
         .leap-metadata-sidebar { padding-left: 0; }
         .hash-badge, .font-mono, code, pre { overflow-wrap: anywhere; word-break: break-word; }
         .semantic-grid { grid-template-columns: 1fr; }
         .semantic-item:nth-child(2) { border-top: 1px solid var(--slate-border); padding-top: 12px; }
         .literate-step { grid-template-columns: 1fr; gap: 6px; }
         .leap-footer { align-items: flex-start; flex-direction: column; }
      }
   </style>

   <div class="leap-page">
      <header class="leap-exec-bar">
         <div class="leap-exec-inner">
            <div style="display:flex; align-items:center; gap:16px;">
               <div class="leap-logo"><img src="_static/leap-axis-logo.svg?v=20260629_01" alt="LEAP AXIS KPI Intelligence System"></div>            </div>
            <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
               <div style="display:flex; align-items:center; gap:8px;">
                  <span class="confidence-dot"></span>
                  <span style="font-size:12px; font-weight:500; color:#64748B;">Discovery Confidence</span>
                  <span style="font-size:14px; font-weight:600; color:var(--success);">90%</span>
               </div>
               <div class="growth-badge">CSHARP</div>
            </div>
         </div>
      </header>

      <main class="leap-main">
         

         <div class="dossier-head">
            <h2>KPI Definition &amp; Lineage</h2>
            <p>Operational KPI record connecting business meaning, ownership, formula, and source evidence</p>
         </div>

         <div class="dossier-grid">
            <div class="stack right-rail">
               <section class="dossier-card business-reading-card">
                  <h3 class="leap-card-title" style="margin-bottom:16px;">Business Reading</h3>
                  <div class="semantic-grid">
                     <div class="semantic-item">
                        <div class="micro-label">Plain-English Meaning</div>
                        <div style="font-size:14px; line-height:1.6;">SOURCE-VERIFIED CANDIDATE: LEAP detected calculation logic named &quot;Cooling Water Delta-T (°C)&quot; in the scanned source.</div>
                     </div>
                     <div class="semantic-item">
                        <div class="micro-label">Decision It Supports</div>
                        <div style="font-size:14px; line-height:1.6;">UNDETERMINED: No explicit business objective found in source file.</div>
                     </div>
                  </div>
                  <div style="margin-top:16px; padding-top:14px; border-top:1px solid var(--slate-border);">
                     <div class="micro-label">Owner's Logic</div>
                     <div style="font-size:14px; line-height:1.6;">If this KPI trends up: Indicates a material change in the measured business condition and should be interpreted with the owner. If it trends down: Indicates a material change in the measured business condition and should be checked against source-data timing. Owner check: What changed in source data, business process, or KPI logic that explains movement in Cooling Water Delta-T (°C)?</div>
                  </div>
               </section>

               <section class="dossier-card system-identifier-card">
                  <h3 class="leap-card-title" style="margin-bottom:16px;">System Identifier</h3>
                  <div class="card-row"><span class="label">KPI_ID:</span><span class="value font-mono">KPI-75403B79EB</span></div>
                  <div class="card-row"><span class="label">Name:</span><span class="value">Cooling Water Delta-T (°C)</span></div>
                  <div class="card-row"><span class="label">Owner:</span><span class="value">Enterprise Data Owner</span></div>
                  <div class="card-row"><span class="label">Last Updated:</span><span class="value font-mono">0.0s (Details 0.0s + Render 0.0s)</span></div>
                  <div class="action-row">
                     
                     <a href="vscode://file/Users/meshaalmouawad/Downloads/AIkpi/sample_project/csv_kpi.cs:1" class="action-btn">VS Code</a>
                     <a href="pycharm://open?file=/Users/meshaalmouawad/Downloads/AIkpi/sample_project/csv_kpi.cs&line=1" class="action-btn">PyCharm</a>
                     
                     <a href="/edit?kpi=Cooling%20Water%20Delta-T%20%28%C2%B0C%29" target="_blank" class="action-btn action-btn-primary">Edit Dossier</a>
                     <a href="#governance-review-note" class="action-btn">Review Extraction</a>
                  </div>
               </section>

               <section class="dossier-card">
                  <h3 class="leap-card-title" style="margin-bottom:16px;">Downstream Usage</h3>
                  <div class="semantic-grid">
                     <div class="semantic-item">
                        <div class="micro-label">Used In KPIs / Reports</div>
                        <div style="font-size:14px; line-height:1.6;"><p>UNDETERMINED: No dashboard, report, or business-process usage mapping found in source file.</p></div>
                     </div>
                     <div class="semantic-item">
                        <div class="micro-label">Input Evidence</div>
                        <div style="font-size:14px; line-height:1.6;"><p>UNDETERMINED: No explicit input-field list found in source file.</p></div>
                     </div>
                  </div>
               </section>

               

               <section class="dossier-card">
                   <div style="display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:16px;">
                      <h3 class="leap-card-title">Mathematical Formulation</h3>
                   </div>
                  <div class="formula-panel">
                     <div class="micro-label">Formal Formula</div>
                     
                     <div class="leap-business-formula-math" data-raw-formula="outlet - inlet"><span class="leap-formula-fallback">outlet - inlet</span></div>
                     
                     
                     <div class="micro-label">Annotated Formula</div>
                     <div class="leap-toggle-container" role="group" aria-label="Formula annotation perspective">
                        <button type="button" class="leap-toggle-btn active" data-perspective="business">Business Interpretation</button>
                        <button type="button" class="leap-toggle-btn" data-perspective="developer">Developer Lineage</button>
                     </div>
                     
                     <div class="leap-annotated-formula-wrapper leap-annotated-equation" data-perspective="business">
                        
                        <div class="leap-formula-node">
                           <span class="leap-math-lbl" data-biz="Outlet" data-dev="COLUMN: outlet">Outlet</span>
                           <div class="leap-math-pointer"></div>
                           <span class="leap-math-render">outlet</span>
                        </div>
                        
                        <div class="leap-formula-node operator-node">
                           <span class="leap-math-lbl" data-biz="Minus" data-dev="OPERATOR: -">Minus</span>
                           <div class="leap-math-pointer"></div>
                           <span class="leap-math-render">-</span>
                        </div>
                        
                        <div class="leap-formula-node">
                           <span class="leap-math-lbl" data-biz="Inlet" data-dev="COLUMN: inlet">Inlet</span>
                           <div class="leap-math-pointer"></div>
                           <span class="leap-math-render">inlet</span>
                        </div>
                        
                     </div>
                     
                     <div class="leap-code-lineage" hidden><div class="leap-code-lineage-title">Developer Lineage Breakdown</div><div class="leap-code-lineage-row"><div class="leap-code-lineage-code">1 | // KPI: Cooling Water Delta-T (°C)</div><div class="leap-code-lineage-role">KPI marker: tells LEAP this nearby code defines or documents a KPI.</div></div><div class="leap-code-lineage-row"><div class="leap-code-lineage-code">2 | public static class CoolingWater</div><div class="leap-code-lineage-role">Source context: supports the KPI definition or execution boundary.</div></div><div class="leap-code-lineage-row"><div class="leap-code-lineage-code">3 | {</div><div class="leap-code-lineage-role">Source context: supports the KPI definition or execution boundary.</div></div><div class="leap-code-lineage-row"><div class="leap-code-lineage-code">4 | public static double DeltaT(double inlet_c, double outlet_c)</div><div class="leap-code-lineage-role">Source context: supports the KPI definition or execution boundary.</div></div><div class="leap-code-lineage-row"><div class="leap-code-lineage-code">5 | {</div><div class="leap-code-lineage-role">Source context: supports the KPI definition or execution boundary.</div></div><div class="leap-code-lineage-row"><div class="leap-code-lineage-code">6 | // ΔT = outlet - inlet</div><div class="leap-code-lineage-role">KPI marker: tells LEAP this nearby code defines or documents a KPI.</div></div><div class="leap-code-lineage-row"><div class="leap-code-lineage-code">7 | return outlet_c - inlet_c;</div><div class="leap-code-lineage-role">Calculation expression: combines source variables used by the formal formula.</div></div><div class="leap-code-lineage-row"><div class="leap-code-lineage-code">8 | }</div><div class="leap-code-lineage-role">Source context: supports the KPI definition or execution boundary.</div></div><div class="leap-code-lineage-row"><div class="leap-code-lineage-code">9 | }</div><div class="leap-code-lineage-role">Source context: supports the KPI definition or execution boundary.</div></div></div>
                     
                     <details class="evidence-inline">
                        <summary>Code Evidence</summary>
                        <pre class="font-mono">   1 | // KPI: Cooling Water Delta-T (°C)
   2 | public static class CoolingWater
   3 | {
   4 |     public static double DeltaT(double inlet_c, double outlet_c)
   5 |     {</pre>
                     </details>
                  </div>
                  <a href="#source-evidence" onclick="openLeapSourceEvidence(event)" style="color:var(--info); font-size:12px; text-decoration:none;">Jump to source evidence</a>
                  <div style="color:var(--slate-muted); font-size:12px; line-height:1.65;">
                     <p>UNDETERMINED: No explicit input-field list found in source file.</p>
                  </div>
               </section>

               

               <section class="dossier-card">
                  <div class="walkthrough-heading">
                     <h3 class="leap-card-title">Literate KPI Walkthrough</h3>
                     <div class="framework-seal" title="Extraction Node Axis: structured path from source code to KPI evidence">
                        <img src="_static/walkthrough-axis-icon.svg?v=20260629_01" alt="Extraction Node Axis">
                     </div>                  </div>
                  <div class="literate-step">
                     <div class="micro-label">Operational Intent</div>
                     <div style="font-size:14px; line-height:1.6;">SOURCE-VERIFIED CANDIDATE: LEAP detected calculation logic named &quot;Cooling Water Delta-T (°C)&quot; in the scanned source. LEAP frames this as an operational evidence signal for enterprise decision-making.</div>
                  </div>
                  <div class="literate-step">
                     <div class="micro-label">Verified Logic Mapping (The Recipe)</div>
                     <div style="font-size:14px; line-height:1.6;"><ol><li>First, LEAP anchors the KPI definition to csv_kpi.cs and classifies the implementation as CSHARP evidence.</li><li>Second, it translates the approved business expression (UNDETERMINED: No approved business formula statement found in source comments.) into the formal MathJax formula shown above.</li><li>Finally, it preserves the executable code context and code fingerprint so future changes to the KPI logic can be detected.</li></ol></div>
                  </div>
                  <div class="literate-step">
                     <div class="micro-label">Logic Safeguards & Validations (The Answers)</div>
                     <div style="font-size:14px; line-height:1.6;"><div class="walkthrough-proof-list"><div class="walkthrough-proof-item"><span class="walkthrough-check">OK</span><div><strong>Source Traceability:</strong> Executable evidence is locked to csv_kpi.cs at line 1.</div></div><div class="walkthrough-proof-item"><span class="walkthrough-check">OK</span><div><strong>Formula Consistency Check:</strong> The business formula and source evidence share compatible calculation structure based on LEAP&#x27;s static comparison.</div></div><div class="walkthrough-proof-item"><span class="walkthrough-check">OK</span><div><strong>Change Detection:</strong> Code Fingerprint 75403b79eb records the current implementation so drift can be detected after regeneration.</div></div><div class="walkthrough-proof-item"><span class="walkthrough-check">OK</span><div><strong>RACI Accountability:</strong> Enterprise Data Owner is assigned as accountable owner for rule confirmation and escalation.</div></div></div></div>
                  </div>
                  <div class="literate-step">
                     <div class="micro-label">Executive Sign-off Alignment</div>
                     <div style="font-size:14px; line-height:1.6;">Business rules are aligned to default rule; no path/name governance match (CSHARP). RACI Owner: Enterprise Data Owner. Consulted reviewer: Domain Subject Matter Expert. Current status: Extracted for validation.</div>
                  </div>
               </section>

               <section class="dossier-card">
                  <h3 class="leap-card-title" style="margin-bottom:16px;">Dependency Decomposition</h3>
                  <div class="dependency-row">
                     <div class="tiny-dot"></div>
                     <div style="flex:1;">
                        <div style="display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap;">
                           <span style="font-size:14px; font-weight:500;">LINEAGE UNDETERMINED: No explicit database schema or variable mapping found in source file.</span>
                           <span class="source-chip">PRIMARY</span>
                        </div>
                        <p style="margin:4px 0 0; color:var(--slate-muted); font-size:12px;">Reporting source inferred from discovered KPI context</p>
                     </div>
                  </div>
                  <div class="dependency-row">
                     <div class="tiny-dot"></div>
                     <div style="flex:1;">
                        <div style="display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap;">
                           <span class="font-mono" style="font-size:13px;">csv_kpi.cs</span>
                           <span class="source-chip" style="color:var(--warning);">SOURCE</span>
                        </div>
                        <p style="margin:4px 0 0; color:var(--slate-muted); font-size:12px;">Line 1 • Comment</p>
                     </div>
                  </div>
                  <div class="dependency-row">
                     <div class="tiny-dot"></div>
                     <div style="flex:1;">
                        <div style="display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap;">
                           <span style="font-size:14px; font-weight:500;">Enterprise</span>
                           <span class="source-chip" style="color:var(--success);">DERIVED</span>
                        </div>
                        <p style="margin:4px 0 0; color:var(--slate-muted); font-size:12px;">Governance domain assigned from rule-based RACI mapping</p>
                     </div>
                  </div>
               </section>

               <section class="dossier-card">
                  <h3 class="leap-card-title" style="margin-bottom:16px;">Semantic Core</h3>
                  <div style="display:grid; gap:16px; font-size:14px;">
                     <div>
                        <div style="color:var(--slate-muted); font-size:12px; font-weight:500; margin-bottom:4px;">DEFINITION</div>
                        <div><p>SOURCE-VERIFIED CANDIDATE: LEAP detected calculation logic named &quot;Cooling Water Delta-T (°C)&quot; in the scanned source. No business meaning was inferred beyond the source text.</p></div>
                     </div>
                     <div>
                        <div style="color:var(--slate-muted); font-size:12px; font-weight:500; margin-bottom:4px;">BUSINESS CONTEXT</div>
                        <div><p>UNDETERMINED: No explicit business objective found in source file.</p></div>
                     </div>
                     <div>
                        <div style="color:var(--slate-muted); font-size:12px; font-weight:500; margin-bottom:4px;">EDGE CASES / COMMENTS</div>
                        <p class="font-mono" style="font-size:12px;">Strict compliance mode: detail generation failed, so LEAP preserved only source-grounded uncertainty statements.</p>
                     </div>
                  </div>
               </section>
               
            </div>

            <aside class="leap-metadata-sidebar">
               <div class="sidebar-card status-card">
                  <h3>System Integrity</h3>
                  <div class="sidebar-status-badge state-validated">
                     <span class="status-dot"></span>
                     Validated
                  </div>
                  <div class="sidebar-meta-row"><span class="meta-label">Sync Window:</span><span class="meta-value">0.0s (Details 0.0s + Render 0.0s)</span></div>
                  <div class="sidebar-meta-row"><span class="meta-label">Confidence:</span><span class="meta-value">90%</span></div>
                  <div class="sidebar-meta-row"><span class="meta-label">Fingerprint:</span><span class="meta-value code-font">75403b79</span></div>
               </div>

               

               <div class="sidebar-card review-queue-card" id="governance-review-note">
                  <h3>Review Queue</h3>
                  <div class="review-status-header">
                     <span class="badge warning-badge">Needs Review</span>
                  </div>
                  <div class="review-message-body">
                     <p class="review-queue-text-display">
                        <strong>Status:</strong> Technical Verification Required
                     </p>
                  </div>
                  <textarea class="review-queue-text" readonly>Please review this LEAP KPI evidence file.&#10;&#10;KPI: Cooling Water Delta-T (°C)&#10;KPI ID: KPI-75403B79EB&#10;Accountable owner: Enterprise Data Owner&#10;Consulted SME: Domain Subject Matter Expert&#10;Source: csv_kpi.cs&#10;Line: 1&#10;&#10;Review questions:&#10;- Does the business meaning match how the KPI is used?&#10;- Does the formula reflect the approved business rule?&#10;- Are the source fields, filters, and reporting period correct?&#10;- Should this KPI be marked Validated or Needs Review?</textarea>
                  <a id="open-email-draft-btn" class="sidebar-btn btn-secondary" href="mailto:?subject=LEAP+KPI+review+requested%3A+Cooling+Water+Delta-T+%28%C2%B0C%29&body=Please+review+this+LEAP+KPI+evidence+file.%0A%0AKPI%3A+Cooling+Water+Delta-T+%28%C2%B0C%29%0AKPI+ID%3A+KPI-75403B79EB%0AAccountable+owner%3A+Enterprise+Data+Owner%0AConsulted+SME%3A+Domain+Subject+Matter+Expert%0ASource%3A+csv_kpi.cs%0ALine%3A+1%0A%0AReview+questions%3A%0A-+Does+the+business+meaning+match+how+the+KPI+is+used%3F%0A-+Does+the+formula+reflect+the+approved+business+rule%3F%0A-+Are+the+source+fields%2C+filters%2C+and+reporting+period+correct%3F%0A-+Should+this+KPI+be+marked+Validated+or+Needs+Review%3F">Open Email Draft</a>
                  <button class="sidebar-btn btn-secondary" type="button" onclick="copyLeapReviewText(this)">Copy Review Text</button>
               </div>
               
               <div class="sidebar-card compact-card">
                  <h3>Extraction Method</h3>
                  <div class="sidebar-meta-row"><span class="meta-label">Type:</span><span class="meta-value">CSHARP + Static Scan</span></div>
                  <div class="sidebar-meta-row"><span class="meta-label">Runtime:</span><span class="meta-value code-font">Offline</span></div>
                  <div class="sidebar-meta-row"><span class="meta-label">Frequency:</span><span class="meta-value code-font">On Demand</span></div>
               </div>
            </aside>
         </div>

      </main>





.. raw:: html

   <hr class="leap-precision-divider">
   <section id="source-evidence" class="leap-source-wrap">
   <details class="source-code-dropdown">
      <summary>View Source Code Context</summary>

.. raw:: html

   <div class="formula-panel" style="background-color: #1E1E2E !important; color: #CDD6F4 !important;">
      <pre class="font-mono" style="background-color: transparent !important; color: #CDD6F4 !important;">// KPI: Cooling Water Delta-T (°C)
public static class CoolingWater
{
    public static double DeltaT(double inlet_c, double outlet_c)
    {
        // ΔT = outlet - inlet
        return outlet_c - inlet_c;
    }
}</pre>
   </div>

.. raw:: html

   </details>
    </section>
    <footer style="background-color: #FAFAFA; border-top: 1px solid #E2E8F0; padding: 48px 24px 24px 24px; font-family: 'Inter', -apple-system, sans-serif; box-sizing: border-box; width: 100%;">

      <div style="max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 32px; padding-bottom: 40px;">

        <div>
          <h5 style="color: #2C3E50; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 16px 0;">Company</h5>
          <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px; font-size: 0.8rem;">
            <li><a href="#" style="color: #718096; text-decoration: none;">About LEAP AXIS</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">News & Press</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">Privacy at LEAP</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">Diversity & Inclusion</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">Accessibility Standard</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">Sustainability Strategy</a></li>
          </ul>
        </div>

        <div>
          <h5 style="color: #2C3E50; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 16px 0;">Developers</h5>
          <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px; font-size: 0.8rem;">
            <li><a href="#" style="color: #718096; text-decoration: none;">KPI Academy</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">GitHub Repository</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">LEAP Open Source Core</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">Data Architecture</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">AST Parser Extensions</a></li>
          </ul>
        </div>

        <div>
          <h5 style="color: #2C3E50; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 16px 0;">Resources</h5>
          <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px; font-size: 0.8rem;">
            <li><a href="#" style="color: #718096; text-decoration: none;">Engineering Blog</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">Industrial Best Practices</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">Deterministic KPI Generators</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">Blueprint Templates</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">Affiliate Integration</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">Resource Library</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">Climate Disclosure Statement</a></li>
          </ul>
        </div>

        <div>
          <h5 style="color: #2C3E50; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 16px 0;">Use Cases</h5>
          <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px; font-size: 0.8rem;">
            <li><a href="#" style="color: #718096; text-decoration: none;">Agile Operations</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">Strategic Enterprise Planning</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">Oil & Gas Systems</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">Educational Infrastructure</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">Healthcare Analytics</a></li>
            <li><a href="#" style="color: #718096; text-decoration: none;">National Security Frameworks</a></li>
          </ul>
        </div>

        <div style="display: flex; flex-direction: column; gap: 16px;">
          <div>
            <h5 style="color: #2C3E50; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 12px 0;">National Alignment</h5>
            <div style="font-size: 0.75rem; color: #718096; line-height: 1.4; border-left: 2px solid #14B8A6; padding-left: 10px;">
              Engineered to support digital transformation pillars of <strong style="color: #2C3E50;">Saudi Vision 2030</strong> and the National Sign-on Platform paradigms.
            </div>
          </div>
          <div style="display: flex; gap: 12px; margin-top: 4px;">
            <a href="#" style="color: #2C3E50; opacity: 0.7;" title="X"><svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a>
            <a href="#" style="color: #2C3E50; opacity: 0.7;" title="YouTube"><svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></a>
            <a href="#" style="color: #2C3E50; opacity: 0.7;" title="Instagram"><svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.051.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z"/></svg></a>
            <a href="#" style="color: #2C3E50; opacity: 0.7;" title="GitHub"><svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg></a>
          </div>
        </div>

      </div>

      <div style="max-width: 1200px; margin: 0 auto; padding-top: 24px; border-top: 1px solid #E2E8F0; display: flex; flex-direction: column; gap: 16px;">

        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
          <div style="font-size: 0.72rem; color: #A0AEC0; line-height: 1.4;">
            <span style="font-weight: 600; color: #2C3E50;">LEAP AXIS Architectural Bluebook</span> &bull; Security State: <span style="color: #14B8A6; font-weight: 600;">AI-NO Offline Mode (Deterministic AST Engine)</span>
          </div>

          <div style="display: flex; gap: 16px; align-items: center; opacity: 0.75; font-size: 0.65rem; font-weight: 600; color: #2C3E50; letter-spacing: 0.05em;">
            <span>SDAIA PDPL</span>
            <span>NCA ECC</span>
            <span>ISO 22400</span>
            <span>SOC 2 TYPE II</span>
            <span>W3C SEMANTIC</span>
            <span>PEP 8 COMPLIANT</span>
          </div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; font-size: 0.72rem;">
          <div style="display: flex; flex-wrap: wrap; gap: 14px; margin: 0; padding: 0;">
            <a href="#" style="color: #718096; text-decoration: none;">Privacy Statement</a>
            <a href="#" style="color: #718096; text-decoration: none;">Terms of Use</a>
            <a href="#" style="color: #718096; text-decoration: none;">Trademarks & IP</a>
            <a href="#" style="color: #718096; text-decoration: none;">Safety & Eco Guidelines</a>
            <a href="#" style="color: #718096; text-decoration: none;">Sitemap</a>
            <a href="#" style="color: #718096; text-decoration: none;">Contract Procurement</a>
            <a href="#" style="color: #718096; text-decoration: none;">Documentation Index</a>
            <a href="#" style="color: #718096; text-decoration: none;">Manage Cookies</a>
            <a href="#" style="color: #718096; text-decoration: none;">Do Not Sell My Info</a>
            <a href="#" style="color: #718096; text-decoration: none;">Modern Slavery Statement</a>
          </div>
          <div style="color: #A0AEC0;">&copy; 2026 LEAP AXIS. All rights reserved.</div>
        </div>

      </div>
    </footer>
	   <script>
	      (function () {
	         function runLeapMathJax(target) {
	            if (!window.MathJax) return;
	            if (window.MathJax.typesetPromise) {
	               window.MathJax.typesetPromise(target ? [target] : undefined).catch(function () {});
	               return;
	            }
	            if (window.MathJax.typeset) {
	               try {
	                  window.MathJax.typeset(target ? [target] : undefined);
	               } catch (error) {}
	            }
	         }
	         function stripOuterParens(value) {
            var text = (value || "").trim();
            while (text.charAt(0) === "(" && text.charAt(text.length - 1) === ")") {
               var depth = 0;
               var balanced = true;
               for (var i = 0; i < text.length; i += 1) {
                  if (text.charAt(i) === "(") depth += 1;
                  if (text.charAt(i) === ")") depth -= 1;
                  if (depth === 0 && i < text.length - 1) {
                     balanced = false;
                     break;
                  }
               }
               if (!balanced) break;
               text = text.slice(1, -1).trim();
            }
            return text;
         }
         function splitTopLevel(value, operators) {
            var text = value || "";
            var depth = 0;
            for (var i = text.length - 1; i >= 0; i -= 1) {
               var ch = text.charAt(i);
               if (ch === ")") depth += 1;
               else if (ch === "(") depth -= 1;
               else if (depth === 0 && operators.indexOf(ch) >= 0) {
                  if (ch === "-" && i === 0) continue;
                  return [text.slice(0, i), ch, text.slice(i + 1)];
               }
            }
            return null;
         }
         function texVariable(value) {
            var text = stripOuterParens(value || "")
               .replace(/`/g, "")
               .replace(/["']/g, "")
               .replace(/\s+/g, " ")
               .trim();
            if (!text) return "";
            if (/^\d+(?:\.\d+)?$/.test(text)) return text;
            return "\\text{" + text.replace(/_/g, " ") + "}";
         }
         function cleanExpression(value) {
            return (value || "")
               .replace(/&amp;/g, "&")
               .replace(/×/g, "*")
               .replace(/÷/g, "/")
               .replace(/\breturn\b\s*/gi, "")
               .replace(/\bNULLIF\s*\(\s*([^,()]+)\s*,\s*0(?:\.0)?\s*\)/gi, "$1")
               .replace(/\bSUM\s*\(\s*([^()]+)\s*\)/gi, "$1")
               .replace(/\bAVG\s*\(\s*([^()]+)\s*\)/gi, "$1")
               .replace(/\bCOUNT\s*\(\s*([^()]+)\s*\)/gi, "$1")
               .trim();
         }
         function expressionToTex(value) {
            var expr = stripOuterParens(cleanExpression(value));
            var split = splitTopLevel(expr, ["+", "-"]);
            if (split) return expressionToTex(split[0]) + " " + split[1] + " " + expressionToTex(split[2]);
            split = splitTopLevel(expr, ["*"]);
            if (split) return expressionToTex(split[0]) + " \\times " + expressionToTex(split[2]);
            split = splitTopLevel(expr, ["/"]);
            if (split) return "\\frac{" + expressionToTex(split[0]) + "}{" + expressionToTex(split[2]) + "}";
            return texVariable(expr);
         }
         function renderBusinessFormula(container) {
            var raw = container.getAttribute("data-raw-formula") || "";
            if (!/[+\-*/×÷]/.test(raw)) return;
            var tex = expressionToTex(raw);
            if (!tex) return;
	            container.innerHTML = "\\[" + tex + "\\]";
	            runLeapMathJax(container);
	         }
	         window.switchLeapMath = function (panel, perspective) {
	            var equation = panel.querySelector(".leap-annotated-equation, .leap-annotated-formula-wrapper");
	            if (!equation) return;
	            equation.setAttribute("data-perspective", perspective);
            var developerMode = perspective === "developer";
            equation.style.backgroundColor = developerMode ? "#F4F6F8" : "";
            var lineage = panel.querySelector(".leap-code-lineage");
            if (lineage) lineage.hidden = perspective !== "developer";
            equation.querySelectorAll(".leap-math-lbl").forEach(function (annotation) {
	               var label = annotation.getAttribute(perspective === "developer" ? "data-dev" : "data-biz");
	               if (label) annotation.textContent = label;
               annotation.style.setProperty("color", developerMode ? "#2C3E50" : "#004E5A", "important");
               annotation.style.setProperty("background-color", developerMode ? "#FFFFFF" : "#E6F0F2", "important");
               annotation.style.setProperty("border-color", "#E1E8ED", "important");
	            });
	            runLeapMathJax(panel);
	         };
         document.querySelectorAll(".formula-panel").forEach(function (panel) {
            var equation = panel.querySelector(".leap-annotated-equation, .leap-annotated-formula-wrapper");
            var buttons = panel.querySelectorAll(".leap-toggle-btn");
            if (!equation || !buttons.length) return;
            buttons.forEach(function (button) {
               button.addEventListener("click", function () {
                  var perspective = button.getAttribute("data-perspective") || "business";
                  window.switchLeapMath(panel, perspective);
                  buttons.forEach(function (candidate) {
                     candidate.classList.toggle("active", candidate === button);
                  });
               });
            });
	         });
	         document.querySelectorAll(".leap-business-formula-math").forEach(renderBusinessFormula);
	         window.addEventListener("DOMContentLoaded", function () {
	            runLeapMathJax();
	         });
	         window.copyLeapReviewText = function (button) {
	            var card = button.closest(".review-queue-card");
	            var text = card ? card.querySelector(".review-queue-text") : null;
	            if (!text) return;
	            text.select();
	            var value = text.value || "";
	            var done = function () {
	               var previous = button.textContent;
	               button.textContent = "Copied";
	               setTimeout(function () { button.textContent = previous; }, 1400);
	            };
	            if (navigator.clipboard && navigator.clipboard.writeText) {
	               navigator.clipboard.writeText(value).then(done).catch(function () {
	                  document.execCommand("copy");
	                  done();
	               });
	            } else {
	               document.execCommand("copy");
	               done();
	            }
	         };
	         window.openLeapSourceEvidence = function (event) {
	            if (event) event.preventDefault();
	            var section = document.getElementById("source-evidence");
	            if (!section) return;
	            var details = section.querySelector("details");
	            if (details) details.open = true;
	            section.scrollIntoView({ behavior: "smooth", block: "start" });
	         };
             
             var hasConflicts = false;
             if (hasConflicts) {
                document.addEventListener("DOMContentLoaded", function() {
                   try {
                      var sidebar = document.querySelector('.leap-metadata-sidebar');
                      var reviewQueue = sidebar ? sidebar.querySelector('.review-queue-card') : null;
                      if (sidebar && reviewQueue) {
                         var alertHtml = '<div class="sidebar-card system-alert-card">' +
                            '<h3>SYSTEM ALERT</h3>' +
                            '<div class="warning-badge">! Needs Review</div>' +
                            '<p><strong>Status:</strong> Technical Verification Required.</p>' +
                            '<div class="gov-conflict-subpanel">' +
                               '<span>GOVERNANCE CONFLICT</span>' +
                               '<p>' +
                                  'ISO Compliance & Governance Conflict:<br>' +
                                  'The operational logic defined by business documentation does not align with the execution path verified in the source repository code.' +
                               '</p>' +
                            '</div>' +
                         '</div>';
                         reviewQueue.insertAdjacentHTML('beforebegin', alertHtml);
                      }
                   } catch (error) {
                      console.error("LEAP Alert Injection Failed:", error);
                   }
                });
             }
      })();
   </script>

   <div id="audit-notes-data" style="display:none;">
      
         <p>Audit Note: Business formula statement is missing or undetermined in source comments.</p>
      
   </div>
   <script>
       // Inject audit notes into Review Queue
       var auditNotes = document.getElementById('audit-notes-data');
       if (auditNotes && auditNotes.innerHTML.trim()) {
           var reviewQueue = document.getElementById('governance-review-note');
           if (reviewQueue) {
               var body = reviewQueue.querySelector('.review-message-body');
               if (body) {
                   body.insertAdjacentHTML('beforeend', auditNotes.innerHTML);
               }
           }
       }
   </script>
   </div>