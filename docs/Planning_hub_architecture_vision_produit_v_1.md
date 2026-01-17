# PlanningHub

## Statut du document

Ce document décrit la **vision produit cible** et l’architecture fonctionnelle complète de **PlanningHub**.

- Il ne représente pas l’état d’implémentation actuel.
- L’ordre de réalisation, le périmètre actif et les dépendances sont définis dans :
  - `docs/roadmap/`
  - `docs/audits/implementation_readiness.md`

Toute implémentation **DOIT** être précédée d’un audit de readiness.

---

Notation utilisée dans ce document :
- **[CORE]** : moteur fondamental requis
- **[ADVANCED]** : nécessite des fondations complètes
- **[FUTURE]** : vision long terme

---

## Architecture & Vision Produit v1.2

### Vision
**PlanningHub = le système nerveux du travail moderne.**

### Principe unificateur
> Tout est une réservation temporelle de valeur.

Chaque engagement (humain, matériel, service) est une occupation d’intervalle temporel avec une valeur économique attachée.

### Mission
Transformer le chaos temporel en orchestration précise du travail.

---

## Structure hiérarchique
```
FOUNDATION -> EXECUTION -> INTELLIGENCE -> SCALE
```
- Core moteurs
- Workflows
- IA & automatisation
- Multi‑organisation

---

## Moteurs du système (architecture microservices)

### 1. Identity & Access Management (IAM)
- User (global) <-> Membership (organisation)
- Rôles & permissions (RBAC / RBAC avancé)
- SSO, OAuth2, MFA
- Audit trail

### 2. Time & Reservation Engine
**SHIFT = temporal_interval + resource_assignment + economic_value**
- Fuseaux horaires (UTC)
- Récurrence (RRULE + exceptions)
- Buffers (setup / teardown)
- Trajets (geo‑aware)

### 3. Conflict Detection & Resolution Engine
Niveaux de priorité :
- **CRITICAL** : violation légale, double booking intra‑org, budget bloquant
- **HIGH** : double booking inter‑org, compétence manquante
- **MEDIUM** : alertes budget, certifications
- **LOW** : préférences, risques d’heures sup

### 4. Resource & Matching Intelligence
```
matching_score = skills*0.35 + availability*0.25 + cost*0.20 + performance*0.15 + proximity*0.05
```
Contextes : emergency, premium, budget

### 5. Execution & Timesheet Engine
Workflow : proposed -> accepted -> confirmed -> in_progress -> completed -> validated -> closed

Effets : notifications, contrats, check‑in/out, timesheets, analytics

### 6. Financial Intelligence Engine
- Coûts estimés vs réels
- Suivi budget projet / mission / shift
- Mise à jour temps réel

### 7. Automation & Intelligence Layer
- Auto‑remplacement
- Alertes budget
- Prévision de demande
- Optimisation planning

### 8. Marketplace & Trust Engine
- Scoring réputation (0‑100)
- Avis multi‑critères
- Résolution de litiges
- Modèles tarifaires flexibles

### 9. Notification & Communication
- Notifications intelligentes
- Digests
- Canaux : in‑app, email, SMS, push, Slack, Teams

### 10. Analytics & Business Intelligence
- Utilisation ressources
- Santé financière
- KPI & prédictions

### 11. Mobile‑first & Offline
- Planning et timesheets offline
- Sync différée
- Check‑in/out mobile

### 12. Sécurité & Conformité
- Chiffrement AES‑256 / TLS 1.3
- GDPR ready
- Audit trail complet

### 13. Intégrations & Écosystème
- Calendriers (Google, Outlook)
- Comptabilité (Sage, Xero, QuickBooks)
- API, Webhooks, SDK

---

## Modèle économique
### Offres
- **Freemium**
- **Starter** : 29 EUR / mois
- **Professional** : 59 EUR / mois
- **Business** : 199 EUR / mois
- **Enterprise** : sur devis

### Revenus
- Abonnements SaaS
- Commissions marketplace
- Options premium IA

---

## Métriques de succès
- DAU > 40%
- Matching accuracy > 85%
- Uptime 99.95%
- NPS > 70

---

## Positionnement
- Source unique de vérité temps / humain / valeur
- IA native et multi‑vertical
- Mobile first, temps réel, financier intégré

