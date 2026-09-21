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
**en cours** (A6).

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
ordre est le dénominateur des exposants locaux de L₃ (2, 2, 3 pour s7) — **en cours** (A1).

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
contre théorie des réseaux, et non la même donnée calculée deux fois. — **en cours** (A2).

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

*Cible vérifiable.* Flèche complète, homomorphisme, injectivité modulo ±1, et quel w_Q fixe quel
lieu — **en cours** (A3). Si elle tient, le drapeau `ATKIN_LEHNER_ACTION_UNVERIFIED` de T3 peut
être proposé à la fermeture (recommandation à T0, pas une édition du checker).

## GE-12 — La règle graduée : l'intégralité dépend de l'unité de mesure

*Image.* On mesure une table en mètres et on trouve 1,5 : « non entier ». On la mesure en
demi-mètres : 3. La table n'a pas changé.

*Pensée.* Le partenaire d'ordre 2 de s10 a des coefficients dyadiques (17/2, 147/2, …) ; celui de
s7 est entier. Faut-il y voir une différence intrinsèque ? La structure Sym² est intrinsèque ;
l'intégralité d'une série dépend de la coordonnée z.

*Résultat — (E), PASS(60), à la main.* Les dénominateurs du partenaire de s10 sont des puissances
pures de 2, d'exposant e(n) < n ; la série en **2z** est entière jusqu'à n < 60. Le partenaire est
donc *globalement borné* avec c = 2.

*Cible vérifiable.* PASS(120), forme close de e(n), même rapport pour s18, et un vrai contre-exemple
(série non globalement bornée) — **en cours** (A4).

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

*Cible vérifiable.* Récupérer et lire les sources, citer mot pour mot ce qui est borné et sous
quelles hypothèses, puis demander à T0 si cela compte comme « base spécifiée » au sens du ledger
(point 4). **Rien n'est exécuté avant sa décision** — **en cours** (B4).

---

## Tableau de bord

| # | image | cible | statut |
|---|---|---|---|
| GE-7 | le promeneur | carte des points ρ = 20 | fait (E/N/L) |
| GE-8 | poussière d'étoiles | critère D carré mod 4n ; complétude | critère fait (E) ; complétude en cours |
| GE-9 | les trois gares | stabilisateurs, ordres 2, 2, 3 | en cours |
| GE-10 | la sphère qui s'évanouit | nodalité sur modèle explicite | en cours — test indépendant |
| GE-11 | le miroir à deux faces | flèche W(n) → O(q) | préliminaire (E) ; en cours |
| GE-12 | la règle graduée | bornitude globale, c = 2 | préliminaire PASS(60) ; en cours |
| GE-13 | le billard d'Artin | métrique indépendante de n | fait (E) ; lecture (C) |
| GE-14 | deux aimants | fourche piège / |D| minimal | énoncée (C) ; à transmettre |
| GE-15 | le budget | sources + décision T0 | en cours ; rien d'exécuté |

*Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: GE-7…GE-9 lus dans les certificats émis
au commit f091e43 ; GE-11…GE-13 calculs à la main de cette session (sympy / Fraction), non encore
revérifiés indépendamment | Reviewed-by: N*
