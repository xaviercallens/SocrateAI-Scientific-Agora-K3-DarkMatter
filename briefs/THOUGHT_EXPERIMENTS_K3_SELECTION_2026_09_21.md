# Expériences de pensée — « quel K3 ? » vu depuis la courbe modulaire : registre et évaluation (2026-09-21)

**Origine.** Demande T0 (Xavier) : consigner les expériences de pensée « à la manière d'Einstein » —
une image simple, poussée jusqu'au bout, qui permet de dialoguer, de raisonner par analogie, et
surtout de savoir **quoi calculer ensuite**. Même format que le registre de Stream 1
(`briefs/THOUGHT_EXPERIMENTS_SELF_DUAL_2026_09_20.md`, GE-1…GE-6) et que `docs/STREAM8_WHICH_K3.md`
de LeanMaster (G1…G10), dont ce document prend la suite côté Stream 2.

**Règle du jeu.** Une expérience de pensée n'est pas un résultat. Chacune est rattachée à une
**cible vérifiable** ; tant que la cible n'est pas atteinte, l'expérience reste une conjecture (C).
Quand l'expérience et le calcul divergent, c'est le calcul qui gagne et la divergence est notée.

Légende : **(K)** noyau Lean (Stream 1 / LeanMaster, lu comme source, aucun build lancé ici) ·
**(E)** calcul exact de ce dépôt · **(N)** reconnaissance numérique à deux précisions ·
**(L)** littérature lue et épinglée · **(M)** connaissance de modèle, source **non** lue — incitable ·
**(C)** conjecture.

**Garde-fous permanents.** Rien ici ne sélectionne un K3. La coupure ρ = 20 n'est pas adoptée
(décision T0 ouverte). Aucune lecture physique n'est revendiquée : une relation géométrique ne
fournit aucun couplage (VISION §1.3), le Tier C reste bloqué (F5b), et la renonciation A-DE (D4)
interdit toute affirmation sur l'énergie noire. Côté s10, tout est indicatif (certificat de réseau
DRAFT).

---

## GE-7 — Le promeneur sur le rail

*Image.* Un promeneur marche le long de la courbe X₀(7)⁺. À chaque pas il porte une surface K3 ; il
regarde son réseau transcendant. Presque partout, il voit le même objet de rang 3, U⊕⟨14⟩. Que
voit-il de spécial, et où ?

*Pensée.* En certains points, un vecteur entier v devient orthogonal à la période : la classe v
« tombe » du côté algébrique, le rang de Picard passe de 19 à 20, et le réseau transcendant se
contracte en un réseau de rang 2, défini positif : T_X = v^⊥.

*Résultat — (E)+(N)+(L).* `CM_POINTS_RHO20.json` : 71 valeurs distinctes de z pour s7, 69 pour s10,
chacune avec son vecteur, son τ exact, sa forme réduite (a,b,c) et son discriminant D. L'arithmétique
des réseaux est exacte ; les valeurs de z sont des reconnaissances numériques (120 → 200 chiffres) à
travers la relation de Hauptmodul certifiée PASS(40) ; le passage « v·ω = 0 ⇒ ρ = 20 » est le cadre
de Dolgachev 1996 §7, lu, non redémontré.

*Évaluation.* **Confirmé comme carte, pas comme sélection.** Voir GE-8.

## GE-8 — La poussière d'étoiles : pourquoi « ρ = 20 » seul ne choisit rien

*Image.* Le promeneur s'attendait à quelques bornes kilométriques. Il découvre que les points
spéciaux sont comme les rationnels sur la droite : il y en a dans tout intervalle, aussi petit
soit-il.

*Pensée.* Les points CM sont denses sur la courbe modulaire **(M)**. « Exiger ρ = 20 » ne découpe
donc aucun morceau de la courbe : topologiquement, cela ne sélectionne rien. Ce qui rend la liste
finie, c'est une **borne sur |D|** — et c'est elle, pas la coupure, qui fait le travail. C'est la
version « courbe » de la leçon G6/G10 de LeanMaster : *nommer la forme définie, et nommer la
coupure qui l'a produite*. Ici il faut ajouter : *et nommer ce qui borne le discriminant*.

*Cible vérifiable.* (i) Critère exact d'occurrence : D apparaît dans la famille de niveau n **ssi**
D est un carré modulo 4n — **(E)**, `A2_MEMBERSHIP.json`, critère = énumération dans les deux sens
pour |D| ≤ 100. (ii) Complétude de la carte D par D, par comptage de formes de Heegner —
**fait (E)**, `CM_COMPLETENESS.json` : pour s7, les 30 discriminants présents dans la table sont
**tous complets** (71 points attendus, 71 trouvés) ; l'incomplétude est entièrement dans les D
*absents* (146 discriminants jusqu'à |D| = 616, le plus petit étant 19), tous hors de la fenêtre
−v² ≤ 44 annoncée. La carte est donc exacte là où elle parle, et muette ailleurs — ce qu'elle
disait d'elle-même.

*Évaluation.* La question mathématique est close : la coupure n'est pas un critère. La question
« qui borne |D| ? » est physique et renvoie à GE-13.

## GE-9 — Les trois gares : le résultat était forcé

*Image.* Sur le rail de s7 il y a exactement trois gares, les trois points singuliers de
l'opérateur : z = 1/27, z = −1, z = ∞. Le promeneur constate que ce sont trois points ρ = 20
(D = −28, −7, −3). Coïncidence remarquable ?

*Pensée.* Non. Une gare est un point **fixé par un élément d'ordre fini** du groupe modulaire. Un
point fixe d'une matrice entière vérifie une équation quadratique entière : il est CM
**automatiquement**. « Les lieux singuliers sont des points ρ = 20 » est un théorème d'une ligne,
pas une découverte — et la troisième gare, que l'estimation à la main n'avait pas anticipée, était
prévisible.

*Résultat — (E)+(N).* Les deux premières lignes étaient prédites avant calcul et confirmées ; la
troisième ne l'était pas, et la clause correspondante de l'estimation est enregistrée **REFUTED**
dans le certificat. Cohérent avec `s7_singular_points_are_selfdual` de Stream 1 **(K)**.

*Cible vérifiable.* Exhiber le stabilisateur entier de chaque gare, son ordre, et vérifier que cet
ordre est le dénominateur des exposants locaux de L₃ — **fait (E)**, `ELLIPTIC_POINTS_ARE_CM.json`.
s7 : ordres **[2, 2, 3]**, générateurs [[0,1],[−7,0]], [[7,−4],[14,−7]], [[2,1],[−7,−3]] ;
s10 (indicatif) : ordres **[2, 2, 4]**. Ils égalent le ppcm des dénominateurs des exposants de L₃
en chaque lieu, et les 68 (resp. 66) points CM qui ne sont pas des gares ont un stabilisateur
trivial — détermination exacte, sans boîte. Contrôle réel : dans le groupe « Fricke seul », la gare
z = ∞ de s10 retombe à l'ordre 2 et z = −1/4 perd son stabilisateur. Le certificat porte la
phrase : *accord forcé, pas corroboration*.

*Leçon.* Même discipline que G10 : un accord **forcé** ne se présente pas comme une corroboration.
Avant de s'émerveiller d'une coïncidence, chercher le théorème d'une ligne qui la rend inévitable.

## GE-10 — La sphère qui s'évanouit : deux sortes de gares

*Image.* Aux gares z = 1/27 et z = −1, le vecteur est une racine : v² = −2. Le promeneur voit une
petite sphère sur sa surface rétrécir jusqu'à disparaître : la surface se pince en un point double.
À la gare z = ∞ (v² = −42), rien ne se pince : la surface reste lisse, elle « tourne » seulement
sur elle-même, d'un tiers de tour.

*Pensée.* Une (−2)-classe orthogonale à la période est un **mur** : la polarisation cesse d'être
ample (Dolgachev Thm 7.3 **(L)**) et le modèle polarisé acquiert un nœud A₁. Un vecteur non
réflexif ne produit aucun mur. Il y aurait donc deux natures de gares : deux gares-murs et une
gare-symétrie. *(Ce n'est pas une lecture de Kodaira : on parle d'un point double de la surface,
pas d'une fibre d'une fibration — ledger, point 3.)*

*Cible vérifiable — la plus importante du registre.* Tester cela sur un **modèle géométrique
explicite** qui n'utilise ni le réseau ni la monodromie (polynôme de Laurent dont les termes
constants donnent s(n), ou les modèles d'Almkvist–van Straten) : valeurs critiques = lieux
singuliers ? point critique non dégénéré (Morse ⇒ nœud A₁) ? combien par valeur ? Ce serait la
**première vérification réellement indépendante** du programme sur ce sujet : géométrie explicite
contre théorie des réseaux, et non la même donnée calculée deux fois.

*Résultat — (E), PASS(10), niveau « modèle ».* `NODALITY_EXPLICIT_MODELS.json`. Trois polynômes de
Laurent admis seulement après vérification exacte de l'identité des termes constants (trois faux
polynômes réels sont refusés). Le texte d'Almkvist–van Straten n'imprime pas d'équations : ses
modèles n'ont pas pu servir.
- **z = 1/27 (s7) et z = 1/16 (s10) : confirmé.** Exactement un point critique, non dégénéré, sur
  le tore ; sur la fermeture (2,2,2), un nœud A₁ nouveau, nombre de Tjurina total 10 → 11.
- **z = −1 (s7) : la clause littérale ÉCHOUE sur ce modèle.** Aucun point critique sur le tore,
  aucun nouveau point singulier : trois nœuds A₁ du bord **fusionnent** en un point étiqueté D₄.
  Le nombre de Tjurina total monte pourtant de +1, comme à z = 1/27. Ce n'est pas une réfutation
  du côté réseau — aucun des modèles n'est le modèle M₇-polarisé — mais la prédiction « un nœud
  apparaît » est fausse telle qu'énoncée, et c'est enregistré.
- **z = −1/4 (s10), sans prédiction : deux nœuds A₁** conjugués sur ℚ(i).
- **z = ∞ : NON EXAMINÉ** (lieu singulier non isolé dans tous les modèles) — dit, pas deviné.
- **Contre-exemple utile :** à z = 1/2, un A₁ devient A₂ (Tjurina +1) alors que L₃ y est régulier.
  Un changement de singularité du modèle ne détecte donc **pas** les points singuliers de
  l'opérateur. Côté réseau, z = 1/2 est un point CM de vecteur non réflexif (−v² = 42, div 7).

*Évaluation.* **Mi-confirmé, mi-corrigé — et plus instructif que prévu.** L'image « une sphère
s'évanouit » décrit bien la gare de divisibilité 1. À la gare de divisibilité 2 (z = −1 ; et
z = −1/4 pour s10) l'image juste semble plutôt : *plusieurs sphères déjà évanouies se rejoignent*
(ou deux s'évanouissent ensemble). Une lecture par systèmes de racines (A₁³ ⊂ D₄ d'indice 2) est
consignée dans le brief comme **hypothèse post hoc : zéro test indépendant passé**.

## GE-11 — Le miroir à deux faces : Atkin–Lehner contre réflexions

*Image.* Pour s10 le groupe a quatre éléments (1, w₂, w₅, w₁₀). Côté réseau, le groupe
discriminant ℤ/20 a lui aussi quatre automorphismes. Jusqu'ici on avait seulement compté :
« 4 = 4 ». Deux salles ayant le même nombre de portes ne sont pas pour autant la même salle.

*Pensée.* Chaque involution a un point fixe ; ce point fixe a un vecteur ; ce vecteur a une
réflexion ; cette réflexion agit sur ℤ/20 par un multiplicateur. On peut donc **construire** la
flèche W(10) → O(q) au lieu de comparer des cardinaux.

*Résultat préliminaire — (E), à la main, non vérifié indépendamment.* Les trois vecteurs des lieux
singuliers de s10, (1,−1,0), (2,−6,1), (10,−10,−3), donnent les multiplicateurs **1, 11, 19** sur
ℤ/20 ; avec −1 ils engendrent tout O(q) = {1, 9, 11, 19}. Le multiplicateur 11 vaut −1 sur la
partie 2-primaire et +1 sur la partie 5-primaire : exactement la forme attendue d'un w_Q.

*Résultat — (E), PASS(30) en n ; identification des z héritée de PASS(40).*
`ATKIN_LEHNER_DISC_FORM.json`, 33 contrôles. La flèche est **construite** à partir de l'action sur
les périodes : le multiplicateur de w_Q sur ℤ/2n vaut −1 modulo 2Q et +1 modulo 2n/Q — dérivé
symboliquement en n, pas cité — et w_Q ↦ m_Q est un **isomorphisme** W(n) → O(q) pour n = 1…30,
Fricke ↦ −1. Pour n = 10 : {1 ↦ 1, w₂ ↦ 11, w₅ ↦ 9, w₁₀ ↦ 19}. Les multiplicateurs à la main
(1, 11, 19) sont confirmés.
- **Réfuté dans mon estimation :** « injective modulo ±1 ». Modulo ±1 le noyau est {1, w_n}.
- **Non anticipé :** w₁₀ fixe z = 1/16, w₅ fixe z = −1/4, mais **z = ∞ n'est le point fixe d'aucune
  involution d'Atkin–Lehner** : il est fixé par des éléments d'**ordre 4** de la classe de w₂ —
  ce qui recoupe l'ordre 4 trouvé en GE-9. w₂ n'a aucune réflexion associée.
- **Monodromie :** les lacets ne réalisent que les multiplicateurs {1, 11} — la moitié de O(q) ;
  9 et 19 n'appartiennent qu'au relèvement algébrique. Pour s7 la monodromie agit trivialement
  modulo ±1 ; pour s10, non.

*Évaluation.* Le « 4 = 4 » devient un isomorphisme explicite. Recommandation à T0 : **resserrer**
le drapeau `ATKIN_LEHNER_ACTION_UNVERIFIED`, pas le fermer (le certificat de réseau de s10 reste
DRAFT ; `check_T3` n'est pas édité). Dans l'image : le miroir a bien deux faces, mais l'une des
gares de s10 n'est pas devant un miroir — elle est sur un **tourniquet à quatre temps**.

## GE-12 — La règle graduée : l'intégralité dépend de l'unité de mesure

*Image.* On mesure une table en mètres et on trouve 1,5 : « non entier ». On la mesure en
demi-mètres : 3. La table n'a pas changé.

*Pensée.* Le partenaire d'ordre 2 de s10 a des coefficients dyadiques (17/2, 147/2, …) ; celui de
s7 est entier. Faut-il y voir une différence intrinsèque ? La structure Sym² est intrinsèque ;
l'intégralité d'une série dépend de la coordonnée z.

*Résultat — (E), PASS(60), à la main.* Les dénominateurs du partenaire de s10 sont des puissances
pures de 2, d'exposant e(n) < n ; la série en **2z** est entière jusqu'à n < 60. Le partenaire est
donc *globalement borné* avec c = 2.

*Résultat — (E), PASS(160), et une borne pour tout n.* `PARTNER_GLOBAL_BOUNDEDNESS.json`. Pour le
partenaire de s10, le plus petit c est **2** ; e(n) = v₂(n!) à l'ordre 160 ; la borne e(n) ≤ n − 1
est **démontrée pour tout n** (√(1+2w) a pour coefficients ±2·Cat(k−1)/2^k, et Σ C(n,k)⁴ ≡ 2ⁿ mod 2),
modulo deux identités que Stream 1 énonce comme théorèmes (`s10_satisfies`, `partner_eq_sqrt_s10`,
lus comme source). s7 : c = 1. s18 : c = 2. Vrais contre-exemples refusés : exp, log(1+z).

*Évaluation.* Recommandation à T0 : C3 demande un L₂ **exhibé sur ℚ** ; la « bornitude globale »
(et la constante c) se **rapporte** comme attribut, elle ne sert pas de porte. La question reste à
T0 ; ce registre ne la tranche pas.

## GE-13 — Le billard d'Artin : ce que « rouler sur le rail » prédit vraiment

*Origine.* Texte externe « Le Rail Modulaire » : l'Univers ne serait pas un cristal gelé, il
« évoluerait le long » de X₀(N)⁺.

*Image.* Prenons l'image au sérieux, comme Einstein poursuivant son rayon de lumière. Un point
matériel libre se déplace sur la courbe. Avec quelle métrique ? L'espace des périodes en porte une,
canonique.

*Résultat — (E), symbolique.* Avec la période de Stream 1, ω(τ) = (1, −nτ², τ) : (ω, ω̄) = 4n·(Im τ)²,
donc K = −2 log Im τ − log 4n, et la métrique vaut 1/(2·(Im τ)²) : **hyperbolique, et indépendante
de n**. Le niveau n n'entre que par une constante additive.

*Pensée poussée au bout — (C)/(M).* (i) Aucun observable tiré du seul terme cinétique ne distingue
s7 de s10 : on retrouve, par un autre chemin, l'aveuglement au candidat constaté par Stream 3.
(ii) Sur une surface hyperbolique d'aire finie, le mouvement libre est ergodique — c'est le billard
d'Artin : la bille ne se pose nulle part. (iii) Avec un frottement (expansion), elle s'arrête là où
elle se trouvait : condition initiale, donc paramètre libre.

*Évaluation.* L'image du rail **explique qu'il reste un paramètre ; elle n'en fixe aucun.** C'est
une anti-sélection. Pour sélectionner, il faut autre chose qu'un rail : un potentiel (GE-15) ou un
piège (GE-14). *Toute lecture de ce scalaire comme quintessence touche la renonciation A-DE : non
faite.*

## GE-14 — Deux aimants, deux gares : la fourche

*Image.* Deux principes physiques connus agissent comme des aimants sur la bille ; on demande à
chacun où il l'attire — **sur notre courbe**, avec nos nombres.

- *Aimant 1 — le piège aux points de symétrie accrue* **(M)** (Kofman et al. 2004 ; Witten 1995 et
  Aspinwall pour K3). Là où une sphère s'évanouit (GE-10), des états deviennent légers et le module
  est capturé. Cet aimant désigne les **gares-murs** : z = 1/27 et z = −1 (D = −28, −7). Atout :
  ensemble fini **sans aucune borne sur |D|**. Faiblesse : avec un champ B égal à ½ sur la sphère,
  le même point est une théorie parfaitement lisse, sans états légers.
- *Aimant 2 — le plus petit trou noir* **(K)** côté LeanMaster (`smallest_black_hole`, G3/G10) : le
  discriminant minimal, D = −3, T_X = A₂. Sur notre courbe : la **gare-symétrie**, z = ∞ — et
  seulement pour s7, car A₂ n'est pas dans la famille s10 **(E)**.

*Évaluation.* **Les deux aimants ne désignent pas la même gare.** C'est une fourche réelle, et
utile : elle transforme « quel K3 ? » en « quel mécanisme ? », et tout argument futur devra dire
lequel il invoque et pourquoi l'autre ne s'applique pas. À transmettre à Stream 1, Stream 3 et
LeanMaster. Rappel de LeanMaster lui-même : *le plus petit trou noir choisit une surface, le vide
non* — l'aimant 2 agit par trou noir, pas sur le vide.

*Lecture de P3 dans cette image — (C).* Le critère « D carré mod 4n » devient une **règle de
sélection sur les charges** : seuls les trous noirs dont le discriminant de charge est un carré
modulo 28 ont leur point attracteur dans la famille s7. C'est un énoncé sur des charges, pas sur le
vide.

## GE-15 — Le budget : qui borne |D| ?

*Image.* GE-8 demandait ce qui borne le discriminant. Un budget fini ferait l'affaire : si chaque
unité de |D| « coûte » quelque chose et que la caisse contient 24, la liste est finie.

*Pensée — (M), sources non lues.* Dans la littérature sur K3×K3 (Aspinwall–Kallosh 2005), les
vides à flux seraient des paires de K3 attractifs et la condition de tadpole χ/24 = 24 bornerait
les données : coupure **et** borne d'un seul coup. Et la F-théorie sur K3×K3 a pour base
B₃ = K3×ℙ¹, qui est une base **spécifiée** — alors que notre WP S3-00b est bloqué faute de B₃.

*Tension à regarder en face.* LeanMaster Stream 9 (S9.5) a montré, dans son cadre T⁶/Γ, que **le
tadpole seul ne borne rien** ; la finitude n'y vient qu'avec une condition de positivité (S9.6b).
Si la même chose vaut ici, le « budget » n'existe qu'accompagné de sa condition de définitude —
retour à G6.

*Résultat — (L), cinq sources récupérées, épinglées, lues ; rien d'exécuté.*
`briefs/T0_DECISION_REQUEST_FLUX_BOUND_ON_D_2026_09_21.md`. **L'image du budget est corrigée en
deux endroits.**
1. *Ce qui est borné n'est pas |D|.* Aspinwall–Kallosh éq. (25) borne ½G² = 24 ; leur preuve de
   finitude borne les six entrées réduites des deux réseaux **conjointement**, en utilisant la
   **définie-positivité** — aucune inégalité « |D| ≤ c » n'est imprimée.
2. *Ce n'est pas le tadpole seul qui borne.* C'est le tadpole **plus** la positivité de la
   supersymétrie : la tension avec Stream 9 (S9.5) se résout en **accord** — K3×K3 est une instance
   de S9.5/S9.6b, pas un contre-exemple. Retour à G6, comme pressenti.
3. *La « liste finie » dépend de la question posée :* 13 paires (G₀ = 0, pas de M2, surfaces
   lisses), 66 (M2 ≥ 0), 313 dans un balayage borné sous d'autres hypothèses — trois problèmes
   différents, pas comparables ; Dasgupta–Rajesh–Sethi exhibent une solution hors des 13 ; et il
   existe une série infinie à direction plate.
4. *Aucune source ne parle d'une famille à un paramètre.* K3×K3 utilise **un membre** isolé, pas
   la famille fibrée ; B₃ = K3×ℙ¹ est la base d'un **autre** modèle (« toy model », disent ses
   auteurs), pas le B₃ manquant de la route Twisted-Weierstrass.

*Évaluation.* **Idée largement dégonflée, et c'est le résultat.** Recommandation du brief :
Q1 (« base spécifiée » ?) **non** ; Q2 (tableau de recoupement ?) **option A — classer**, B
seulement si T0 veut le tableau, avec pré-enregistrement et contrôle de taux de base. WP S3-00b
reste BLOQUÉ. Leçon d'image : le budget existe, mais la caisse n'a un fond que si la physique
fournit d'abord une forme définie ; et appartenir à *une* des listes ne dit presque rien, puisque
la liste change avec la question.

---

## Tableau de bord

| # | image | cible | statut |
|---|---|---|---|
| GE-7 | le promeneur | carte des points ρ = 20 | fait (E/N/L) |
| GE-8 | poussière d'étoiles | critère D carré mod 4n ; complétude | **fait** — table complète là où elle parle (30/30 D, 71/71 points) |
| GE-9 | les trois gares | stabilisateurs | **fait** — ordres [2,2,3] (s7), [2,2,4] (s10) ; accord forcé |
| GE-10 | la sphère qui s'évanouit | nodalité sur modèle explicite | **mi-confirmé** (z = 1/27, 1/16) ; **clause fausse** à z = −1 (fusion A₁³ → D₄) ; z = ∞ non examiné |
| GE-11 | le miroir à deux faces | flèche W(n) → O(q) | **fait** — isomorphisme, PASS(30) ; z = ∞ de s10 fixé par un ordre 4, pas une involution ; « injective mod ±1 » réfuté |
| GE-12 | la règle graduée | bornitude globale | **fait** — c = 2 (s10, s18), c = 1 (s7) ; e(n) ≤ n−1 pour tout n |
| GE-13 | le billard d'Artin | métrique indépendante de n | fait (E) ; lecture (C) |
| GE-14 | deux aimants | fourche piège / \|D\| minimal | énoncée (C) ; à nuancer par GE-10 : la « gare-mur » z = −1 n'est pas un simple nœud sur le modèle examiné |
| GE-15 | le budget | sources + décision T0 | **lu, dégonflé** — ce qui borne est tadpole + positivité, pas \|D\| ; recommandation : classer |

## Ce que les calculs ont appris aux images

1. **Trois de mes estimations à la main ont été réfutées** (z = ∞ « pas un point singulier » ;
   « un nœud apparaît à z = −1 » ; « injective modulo ±1 ») et une idée entière (GE-15) a été
   corrigée par la lecture des sources. Aucune n'a été cachée ; chacune a appris quelque chose.
2. **La divisibilité du vecteur compte autant que sa norme.** Div 1 : un nœud naît. Div 2 : des
   nœuds fusionnent ou naissent par paires. C'est le fil à tirer ensuite (hypothèse, zéro test).
3. **s10 a une gare d'ordre 4** que ni Fricke ni aucune involution d'Atkin–Lehner ne voit : deux
   calculs indépendants (GE-9, GE-11) tombent dessus.
4. **Un accord ne vaut que si les routes diffèrent** : GE-9 est forcé ; GE-10 est la seule route
   vraiment indépendante — et c'est justement elle qui a contredit une prédiction.

*Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: GE-7…GE-8 certificats au commit
f091e43 ; GE-8(ii)…GE-12 certificats émis au commit b636f08, chacun construit par un agent et
re-dérivé par un vérificateur indépendant (producteur ≠ vérificateur) ; GE-13 calcul symbolique de
cette session, non revérifié indépendamment ; GE-15 cinq sources lues et épinglées
(`docs/literature/MANIFEST.md`, addendum du 2026-09-21) | Reviewed-by: N*
