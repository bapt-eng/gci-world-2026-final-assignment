# Architecture des 15 Slides Exécutives : Company A
**Titre :** *Value-Driven Retention & Predictive Device Upgrade*  
**Auteur :** Baptiste Bedeaux (`BaptisteBdx`)  
**Format :** Présentation stratégique pour le Comité de Direction (Board) de Company A (15 slides max).

---

### Structure Détaillée Diapositive par Diapositive

| N° | Titre de la Slide | Type de Contenu & Graphiques Clés | Message Stratégique / Chiffres Clés |
| :---: | :--- | :--- | :--- |
| **1** | **Titre & Enjeu Exécutif** | Page de garde premium avec logos et sous-titre clair. | Comment endiguer une hémorragie de 34,4 M$ d'ARR grâce à une rétention ciblée par la valeur. |
| **2** | **Contexte Sectoriel & Marché Télécom** | Graphique comparatif SAC (350$) vs SRC (75$) sourcé GSMA 2025. | Le marché est saturé (>110% de pénétration) : conserver un abonné rentable coûte 4 à 5 fois moins cher qu'en acquérir un nouveau. |
| **3** | **Diagnostic de Company A : L'Hémorragie Cachée** | Waterfall chart montrant le CA brut vs les 34,45 M$ d'ARR perdus par le churn (49,56%). | L'opérateur perd un client sur deux chaque année ; la moitié du cash-flow est constamment érodée. |
| **4** | **L'Illusion du Churn Homogène** | Graphique de dispersion : Churn Rate vs ARPU par décile client. | Tous les clients ne se valent pas : les 20% des clients les plus rentables génèrent plus de 50% de la marge opérationnelle. |
| **5** | **Le Déclencheur Opérationnel n°1 : L'Âge de l'Équipement** | Graphique à barres : Churn rate en fonction de `eqpdays` (< 1 an : 45% -> > 2 ans : 58%). | Le matériel obsolète est le signal physique majeur de résiliation (+12,7 points d'attrition au-delà de 2 ans). |
| **6** | **Les Facteurs Secondaires : Friction Réseau & Facturation** | Matrice de corrélation : appels coupés (`drop_vce`), friction support (`custcare`) et surcoûts (`ovrrev`). | L'inconfort réseau et les dépassements de forfait imprévus ("Bill shock") accélèrent le départ des clients fragiles. |
| **7** | **L'Approche Prédictive : Modélisation Machine Learning** | Schéma d'architecture du pipeline ML (Nettoyage, Encodage, Validation croisée 5-folds). | Déploiement de modèles prédictifs pour anticiper le churn de 30 à 60 jours avant l'acte de résiliation. |
| **8** | **Comparatif des Modèles & Métriques Officielles** | Tableau de score : Baseline Régression Logistique vs Random Forest vs LightGBM (ROC-AUC, Precision, Recall). | **LightGBM surperforme avec un ROC-AUC de 0.695** et un Lift x2.4 sur le décile supérieur (critère officiel obligatoire). |
| **9** | **Feature Importance : Les Véritables Leviers d'Action** | Diagramme d'importance des variables (Gain / SHAP). | Distinction nette entre les variables démographiques non actionnables et les leviers actionnables (`eqpdays`, `change_mou`, `ovrrev`). |
| **10** | **Le Concept Clé : Expected Revenue at Risk (ERaR)** | Heatmap 2D : Probabilité de Churn ($P$) × Valeur Client (ARPU). | Définition de la cible d'intervention prioritaire : haute probabilité de départ ET forte valeur résiduelle. |
| **11** | **La Recommandation Stratégique : Programme "5G Device Upgrade"** | Mockup de l'offre commerciale proposée au client (Smartphone subventionné + 24 mois d'engagement). | Transformer un risque de churn en un réengagement ferme de deux ans avec montée en gamme forfaitaire. |
| **12** | **Modèle Financier & Analyse de Rentabilité (Business Case)** | Tableau de rentabilité financière : Coût unitaire (120$) vs Valeur sauvée (1 400$ sur 24 mois). | **Investissement : 1,8 M$ | Marge nette sauvée : 7,2 M$ | ROI net : 300% | Payback : 4,2 mois.** |
| **13** | **Plan de Déploiement Opérationnel (Roadmap 12 Mois)** | Gantt chart / Timeline en 3 phases (M1-M3 Pilote 5k -> M4-M6 Déploiement -> M7-M12 Automatisation CRM). | Une exécution progressive et maîtrisée sans risque de dépassement budgétaire. |
| **14** | **Gouvernance des Risques & Limites du Modèle** | Matrice de mitigation des risques (Effet d'aubaine / Cannibalisation, Défaillance logistique, Biais algorithmique). | Précautions indispensables pour préserver la confiance des actionnaires et des régulateurs. |
| **15** | **Conclusion & Prochaines Décisions du Board** | Synthèse des 3 décisions immédiates requises lors du conseil d'administration. | Approbation du budget pilote de 600 k$ pour lancer le trimestre 1. |

---

### Annexe : Citations & Sources Officielles (Slide 15 / Champ Omnicampus)
1. **GSMA Intelligence (2025)** : *The Mobile Economy & Global Churn Dynamics*.
2. **Analysys Mason (2024)** : *Telecom Customer Acquisition Costs vs Retention Strategies in Saturated Markets*.
3. **Federal Communications Commission (FCC, 2024)** : *Annual Mobile Wireless Competition Report*.
4. **Matsuo-Iwasawa Laboratory (2026)** : *GCI World 2026 September Course Materials & Dataset Overview*.
